from flask import Flask, flash, render_template, request, redirect, url_for, session
import model.users as users
import model.transactions as transactions

app = Flask(__name__)
app.secret_key = 'people_in_paris'

@app.route("/", methods=["GET"])
def starting_point():
    return render_template("main.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_user.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = users.User.from_db(username)
        if user and user.password == password:
            # Class methode wird aufgerufen um isLoggedIn zu updaten
            users.User.login(username) 
            session['username'] = user.username
            flash("Logged in successfully!", "success")
            return redirect(url_for('hello_user', username=user.username))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('login'))

#Abmelden
        
@app.route("/logout")
def logout():
    username = session.get('username')
    if username:
        user = users.User.from_db(username)
        if user:
            users.User.logout(username)
            session.pop('username', None)
            flash("Logged out successfully!", "success")
    return redirect(url_for('starting_point'))

#Userinfos

@app.route("/getUser/<string:username>")
def get_user(username):
    user = users.User.from_db(username)
    if user:
        return f"User found: {user.username}, {user.firstname}, {user.lastname}"
    else:
        return "User not found"

#Neuen user festlegen

@app.route("/addUser", methods=["GET", "POST"])
def user_form():
    if request.method == "GET":
        return render_template("add_user.html")
    else:
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        password = request.form.get("password")
        amount = int(request.form.get("amount"))
        isLoggedIn = 0
        user = users.User(username, firstname, lastname, password, amount, isLoggedIn)
        user.to_db()
        flash("User added successfully!", "success")
        return render_template("main.html")

#Willkommensnachricht
    
@app.route("/hello/<string:username>")
def hello_user(username):
    user = users.User.from_db(username)
    if user:
        return render_template(
            "user_menu.html",
            title="Hello",
            user=user.username,
            amount=user.amount
        )
    else:
        flash("User not found", "danger")
        return redirect(url_for('starting_point'))

#User-transaktionen
@app.route("/transaction", methods=["GET", "POST"])
def add_transaction():
    if request.method == "GET":
        user = users.User.get_logged_in_user()  
        if user:
            return render_template("make_transaction.html", user=user)
        else:
            flash("User not logged in", "danger")
            return redirect(url_for('starting_point'))
    elif request.method == "POST":
        sendingUsername = request.form.get("sending_username")
        receivingUsername = request.form.get("receiving_client")
        transactionAmount = int(request.form.get("transaction_amount"))

        sender = users.User.from_db(sendingUsername)
        receiver = users.User.from_db(receivingUsername)

        if sender and sender.isLoggedIn:
            if sender.amount >= transactionAmount:
                users.User.update_amount(sendingUsername, sender.amount - transactionAmount)
                users.User.update_amount(receivingUsername, receiver.amount + transactionAmount)
                transaction = transactions.Transaction(sendingUsername, receivingUsername, transactionAmount)
                transaction.to_db()
                flash(f"Transaction from {sendingUsername} to {receivingUsername} for amount {transactionAmount} processed", "success")
                return redirect(url_for('hello_user', username=sendingUsername))
            else:
                flash("Insufficient funds", "danger")
                return redirect(url_for('hello_user', username=sendingUsername))
        else:
            flash("Sender is not logged in or does not exist", "danger")
            return redirect(url_for('starting_point'))


app.run()
