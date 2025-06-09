# main.py
import os
from flask import Flask, render_template
from datetime import datetime
from flask import render_template

port = int(os.environ.get("PORT", 8080))
app = Flask(__name__, template_folder=os.path.join("..", "frontend", "templates"))

# This route will render the index.html template with a name variable
@app.route("/")
def hello():
    return render_template("index.html")
def ask():
    data = request.json
    user_input = data.get("user_input", "")
    return render_template("index.html", name=user_input)

# This route will greet the user based on the username provided in the URL
@app.route("/<username>")
def greet_user(username):
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    return f"{greeting}, {username.capitalize()}!"

#This ensures that the Flask app runs when this script is executed directly
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
