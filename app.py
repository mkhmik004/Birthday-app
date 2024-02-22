import os
import uuid
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

app.secret_key = "1qsdew23456789ol.,kmnbv456789op;.2345678900-=['/']\'[;/.mnbvc`aq§23r9=[34jti1234567890=]\/.,utio3jrke,fv/vlb\]'pl]"

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure Flask session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)  # Initialize Session with app

@app.route("/", methods=["GET", "POST"])
def index():
    # Generate a unique identifier for the user if it doesn't exist in the session
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # Generate a unique identifier for the user

    if request.method == "POST":
        # Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get('month')
        day = request.form.get("day")
        db.execute("INSERT INTO birthdays (name, month, day, user_id) VALUES (?, ?, ?, ?)", name, month, day, session['user_id'])
        flash(f"You've successfully added {name}'s birthday", "success")
        return redirect("/")
    else:
        # Display the entries in the database for the current user
        rowEntries = db.execute("SELECT * FROM birthdays WHERE user_id = ?", session['user_id'])
        return render_template("index.html", rowEntries=rowEntries)

@app.route("/remove", methods=["POST"])
def remove():
    id = request.form.get("id")
    db.execute("DELETE FROM birthdays WHERE id = ? AND user_id = ?", id, session['user_id'])
    flash("You've successfully removed a birthday", "danger")
    return redirect("/")

@app.route("/edit", methods=["POST", "GET"])
def edit():
    if request.method == "GET":
        variables = {'id', 'name', 'month', 'day'}
        for variable in variables:
            session.pop(variable, None)
        session['id'] = request.args.get("id")
        session['name'] = request.args.get('name')
        session['month'] = request.args.get('month')
        session['day'] = request.args.get("day")
        return render_template("edit.html", id=session.get('id'), name=session.get('name'), month=session.get('month'), day=session.get('day'))
    else:
        id = session.get("id")
        day = request.form.get("day")
        name = request.form.get("name")
        month = request.form.get("month")
        stuff = {name, day, month}
        for thing in stuff:
            if not thing:
                thing = session.get(thing)
        db.execute("UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id = ? AND user_id = ?", name, int(month), int(day), int(id), session['user_id'])
        flash(f"You've successfully edited {name}'s birthday details", "warning")
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
