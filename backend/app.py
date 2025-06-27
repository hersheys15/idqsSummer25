# main.py
import os
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask import render_template
from llm_handling import generate_response
from flask_cors import CORS

port = int(os.environ.get("PORT", 8080))
app = Flask(__name__, template_folder=os.path.join("..", "frontend", "templates"))
CORS(app, resources={r"/ask": {"origins": "*"}})  # allows any frontend to access /ask

# This route will render the index.html template with a name variable
@app.route("/")
def hello():
    return render_template("index.html")

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

# This route will handle the LLM response generation
@app.route("/generate/<prompt>")
def generate(prompt):
    # Call the generate_response function from llm_handling.py
    response = generate_response(prompt)
    
    # Return the generated response
    return response

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    #print("Received POST data:", data)  # Add this line
    user_input = data.get("message", "")
    response = generate_response(user_input)
    return jsonify({"response": response})

#This ensures that the Flask app runs when this script is executed directly
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
