from flask import Flask, render_template, request, redirect, url_for
import graphql_helper
import json

app = Flask(__name__)


@app.route("/")
def index():
    list_data = graphql_helper.get_list_data()

    # sorts list by list id then item id so it will render the same way
    list_data.sort(key=lambda x: x["listid"])
    for item in list_data:
        item["items_collection"].sort(key=lambda x: x["itemid"])

    return render_template("index.html", list_data=list_data)


@app.route("/add_item", methods=["POST"])
def add_item():
    item_name = request.form["itemname"]
    list_id = request.form["listid"]

    response = graphql_helper.add_item(item_name, list_id)

    if response.get("data"):
        return redirect(url_for("index"))
    else:
        return "Error adding item."


@app.route("/add_list", methods=["POST"])
def add_list():
    list_name = request.form["listname"]

    response = graphql_helper.add_list(list_name)

    if response.get("data"):
        return redirect(url_for("index"))
    else:
        return "Error adding catagory."


@app.route("/delete_item", methods=["POST"])
def delete_item():
    itemid = request.form["itemid"]

    response = graphql_helper.delete_item(itemid)

    if response.get("data"):
        return redirect(url_for("index"))
    else:
        return "Error deleting item."


@app.route("/edit_item", methods=["POST"])
def edit_item():  # rename edit_item
    item_id = request.form["itemid"]
    item_name = request.form["itemname"]
    list_id = request.form["listid"]

    response = graphql_helper.edit_item(item_id, item_name, list_id)

    if response.get("data"):
        return redirect(url_for("index"))
    else:
        return "Error editing item."


@app.route("/edit_list", methods=["POST"])
def edit_list():
    listid = request.form["listid"]
    new_list_name = request.form["listname"]

    response = graphql_helper.edit_list(listid, new_list_name)

    if response.get("data"):
        return redirect(url_for("index"))
    else:
        return "Error editing catagory."


@app.route("/delete_list", methods=["POST"])
def delete_list():
    list_id = request.form["listid"]

    response = graphql_helper.delete_list(list_id)

    if response.get("data"):
        return redirect(url_for("index"))
    else:
        return "Error editing catagory."


if __name__ == "__main__":
    app.run(debug=True)