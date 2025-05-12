# main.py
import os
from flask import Flask

port = int(os.environ.get("PORT", 8080))
app = Flask(__name__)

@app.route("/")
def home():
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
