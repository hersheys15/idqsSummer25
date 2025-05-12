# main.py
import os
from flask import Flask
from datetime import datetime
from flask import render_template

port = int(os.environ.get("PORT", 8080))
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html", name="Ashvik")

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
