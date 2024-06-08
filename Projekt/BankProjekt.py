from flask import Flask
from flask import render_template
from flask import request
import users

app = Flask(__name__)

@app.route("/") #oder dein dein eigener Pfad
def hello_world():  # beliebiger Funktionsname
    return "Hello world" # Der Text der unter der Route angezeigt wird.

@app.route("/hello/<string:username>")
def hello_user(username):
    return render_template(
        "template.html",
        title = "Hello",
        user = username
    )

@app.route("/add_user", methods=["GET", "POST"])
def user_form():
    if request.method == "GET":
         return '''<form method="POST">
                      <div><label>Username: <input type="text" name="username"></label></div>
                      <div><label>Firstname: <input type="text" name="first_name"></label></div>
                      <div><label>Lastname: <input type="text" name="last_name"></label></div>
                      <input type="submit" value="Submit">
                  </form>'''
    else:
        username = request.form.get("username")
        firstname = request.form.get("first_name")
        lastname = request.form.get("last_name")
        user = users.User(username, firstname, lastname)
        user.to_db()
        return f"Benutzer {username} wurde hinzugefügt"