# devii_python_tutorial

## This tutorial will use Python, Flask, Jinja2, HTML, Javascipt, and a SQL database to create a todo app.

Before you proceed further with the tutorial you need to ensure that you have Python installed.

- Windows:

  - Open the command prompt and type ‘python --version or python -V’ if you have python installed you will receive a response “Python 3.x.x”, the 3.x.x represents the python version you have installed.

- macOS and Linux:

  - If you have a mac, open the Terminal app by going to the Applications folder or Spotlight search and searching for Terminal, type ‘python --version or python -V’ if python is installed you will see a response

“Python 3.x.x”, the 3.x.x represents the python version you have installed.

If you do not have python installed, please visit https://www.python.org/ and follow the instructions to download the appropriate version for your OS.

### **Once you have confirmed you have python installed, clone this repository and follow the instructions below**

NEXT,

Create a python virtual environment, this will isolate project dependencies and avoid conflicts with other projects.

Run the following command to create a virtual environment named "venv" (OS agnostic):

    python -m venv venv

  or

    python3 -m venv venv

If running Windows run this command to activate your venv:

    venv\Scripts\activate

if running mac or linux run this command to activate your venv:


    source venv/bin/activate

THEN, run

    pip install -r requirements.txt

FINALLY, to run the project

Windows:

    python app.py

Linux:

    flask run

The app should be running on your local server http://127.0.0.1:5000
