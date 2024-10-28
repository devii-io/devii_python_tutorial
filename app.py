from flask import Flask, flash, render_template, request, redirect, url_for
import graphql_helper
import utils
import auth
import register
import json

app = Flask(__name__)


@app.route('/', methods=['GET']) 
# get method to render the index page
def index():
    return render_template('index.html')    

@app.route('/login', methods=['GET'])
# get method to render the login form
def login_form():
    return render_template('login.html')

@app.route('/login', methods=['POST'])  
# post method to login
def login():
    email = request.form['username']
    password = request.form['password']
    tenantid = request.form['tenantid']
    data = {
        "login": email,
        "password": password,
        "tenantid": tenantid
    }

    # Call ensure_token_exists and get the status code and message
    token_status = auth.ensure_token_exists(data)
    
    if token_status["status_code"] == 200:
        return redirect(url_for('home'))
    else:
        return f"Error: {token_status['message']}", token_status["status_code"]


@app.route("/signup", methods=["GET"])
# get method to render the signup form
def signup_form():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
# post method to create a new user
def signup():   
    # the variables will be retrieved from a form the user will submit
    name = request.form["name"]
    email = request.form["username"]
    password = request.form["password"]
    tenantid = request.form["tenantid"]
    data = {       
        "name": name,
        "login": email,
        "password": password,
        "tenantid": int(tenantid)
    }
    #register.anon_login will return an access token for the anonymous user to create a new user
    access_token = register.anon_login(tenantid)
    
    if access_token:
        #register.create_user will create a new user if the access token is valid
        if register.create_user(data, access_token):
            return redirect(url_for("login"))
        else:
            flash("User creation failed. Please try again.")
            return redirect(url_for("signup"))
    else:
        flash("Anonymous login failed. Please try again.")
        return redirect(url_for("signup"))
    

@app.route("/logout")   
def logout():
    response = auth.logout()
    if response.get("status") == "success":
        return redirect(url_for("login"))  
    
    


@app.route("/home")

#this is the home page for the app
def home():
    #this will get all the data from your database via Devii
    list_data = graphql_helper.get_list_data()

    status_data = graphql_helper.get_status_name()

    # sorts list by list id then item id so it will render the same way
    list_data.sort(key=lambda x: x["listid"])
    for item in list_data:
        item["item_collection"].sort(key=lambda x: x["itemid"])
    
    # this returns the home.html template with the list data
    return render_template("home.html", list_data=list_data, status_data=status_data)


@app.route("/add_item", methods=["POST"])
# this will be the Add Item route 
def add_item():
    print("add_item")
    # items will be added via a form made in the home.html 
    item_name = request.form["itemname"]
    list_id = request.form["listid"]
    status_id = request.form["statusid"]

    # The response will add the item to your database and add the list_id as the FK for that item
    response = graphql_helper.add_item(item_name, list_id, status_id)

    # each GraphQL query or mutation will send a nested json response back, the first key 
    # will be "data", if the response detects that key it will redirect to the home page and 
    # refresh the list_data
    if response.get("data"):
        return redirect(url_for("home"))
    else:
        return "Error adding item."


@app.route("/add_list", methods=["POST"])
def add_list():
    list_name = request.form["listname"]
    status_id = request.form["statusid"]

    response = graphql_helper.add_list(list_name, status_id)

    if response.get("data"):
        return redirect(url_for("home"))
    else:
        return "Error adding category."


@app.route("/delete_item", methods=["POST"])
def delete_item():
    itemid = request.form["itemid"]

    response = graphql_helper.delete_item(itemid)

    if response.get("data"):
        return redirect(url_for("home"))
    else:
        return "Error deleting item."


@app.route("/edit_item", methods=["POST"])
def edit_item(): 
    item_id = request.form["itemid"]
    item_name = request.form["itemname"]
    list_id = request.form["listid"]
    status_id = request.form["statusid"]

    response = graphql_helper.edit_item(item_id, item_name, list_id, status_id)

    if response.get("data"):
        return redirect(url_for("home"))
    else:
        return "Error editing item."


@app.route("/edit_list", methods=["POST"])
def edit_list():
    listid = request.form["listid"]
    new_list_name = request.form["listname"]
    statusid = request.form["statusid"]

    response = graphql_helper.edit_list(listid, new_list_name,statusid)

    if response.get("data"):
        return redirect(url_for("home"))
    else:
        return "Error editing category."


@app.route("/delete_list", methods=["POST"])
def delete_list():
    list_id = request.form["listid"]

    response = graphql_helper.delete_list(list_id)

    if response.get("data"):
        return redirect(url_for("home"))
    else:
        return "Error editing category."

@app.route("/get_status", methods=["GET", "POST"])
def get_status():
    status_data = graphql_helper.get_status_name()

    return status_data

#The "GET" method is used here to ensure a response from GraphQL
@app.route("/introspection", methods=["GET"])
def introspect():
    try:
    # Run the devii_introspect function and get messages
        messages = utils.devii_introspect()
        

        # You can return additional data if needed
        result = {"status": "success", "messages": messages}
    except Exception as e:
        # Handle exceptions if introspection fails
        result = {"status": "error", "message": str(e)}
    print ("flask result: ", messages)
    return result

if __name__ == "__main__":
    app.run(debug=True)
