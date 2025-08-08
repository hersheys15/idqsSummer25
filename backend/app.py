# main.py
import os, json, requests
from flask import Flask, render_template, request, jsonify, Response, stream_with_context, render_template
from datetime import datetime
from llm_handling import generate_response
from flask_cors import CORS

port = int(os.environ.get("PORT", 8080))
app = Flask(__name__, template_folder=os.path.join("..", "frontend", "templates"))
CORS(app, resources={r"/ask": {"origins": "*"}})  # allows any frontend to access /ask

# This route will render the index.html template with a name variable
@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("message", "")
    
    return Response(
    stream_with_context(generate_response(user_input, stream=True)),
    content_type="text/plain"
    )

#This ensures that the Flask app runs when this script is executed directly
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    