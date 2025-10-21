from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_session import Session
from model import granite_generate_response
from textblob import TextBlob
# IBM Watsonx AI imports
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# IBM watsonx credentials
API_KEY = "c7f6wBkqUmkmyfbA4gmQAYGOLbiqBBhwP2nzr7elWFIS"
PROJECT_ID = "7d3f943c-f7aa-449b-9a3c-883516123e62"
# For ibm-watsonx-ai package, we need to construct the URL
URL = "https://us-south.ml.cloud.ibm.com"  # Dallas region URL

# Connect to IBM watsonx
try:
    credentials = Credentials(
        api_key=API_KEY,
        url=URL
    )
    # Initialize the model with a supported model
    model = ModelInference(
        model_id="ibm/granite-3-8b-instruct",  # Using a supported model
        credentials=credentials,
        project_id=PROJECT_ID
    )
    ibm_client_available = True
except Exception as e:
    print(f"IBM Watsonx AI initialization failed: {e}")
    ibm_client_available = False

# Simple cache for common questions (to reduce API costs)
response_cache = {
    "hello": "Hello! I'm your CitizenAI assistant. How can I help you today?",
    "hi": "Hi there! I'm your CitizenAI assistant. What can I do for you?",
    "how are you": "I'm just a computer program, but I'm functioning well! How can I assist you today?",
    "what can you do": "I'm an AI assistant for CitizenAI, a civic engagement platform. I can help answer questions about civic services, community issues, and government processes.",
    "who are you": "I'm the CitizenAI assistant, here to help you with civic engagement and community-related questions."
}

# In-memory storage
chat_history = []
sentiments = []
concerns = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    response, sentiment, submitted = "", "", False

    if request.method == "POST":
        if "question" in request.form:
            question = request.form["question"]
            response = granite_generate_response(question)
            chat_history.append((question, response))

        elif "feedback" in request.form:
            feedback = request.form["feedback"]
            # Fix for TextBlob polarity issue
            blob = TextBlob(feedback)
            polarity = blob.sentiment.polarity
            sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
            sentiments.append(sentiment)

        elif "concern" in request.form:
            concern = request.form["concern"]
            concerns.append(concern)
            submitted = True

    return render_template("chat.html", history=chat_history, sentiment=sentiments[-1:] if sentiments else None, concern_submitted=submitted)

# New route for AI chatbot
@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        # Get the JSON message from the frontend
        data = request.get_json()
        user_message = data.get("message", "") if data else ""
        
        # Convert to lowercase for cache matching
        user_message_lower = user_message.lower().strip()
        
        # Check cache first to reduce API costs
        if user_message_lower in response_cache:
            return jsonify({"reply": response_cache[user_message_lower]})
        
        # Check if IBM client is available
        if not ibm_client_available:
            fallback_response = f"I understand your question about '{user_message}'. Unfortunately, I'm currently unable to access the IBM Watsonx AI service. Please check the configuration or try again later."
            return jsonify({"reply": fallback_response}), 200
        
        # Send message to IBM Watsonx AI
        prompt = f"You are a helpful assistant for a civic engagement platform called CitizenAI. {user_message}"
        response = model.generate(prompt=prompt, params={
            "decoding_method": "greedy",
            "max_new_tokens": 300,
            "min_new_tokens": 10,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 1
        })
        
        # Extract the AI's reply
        ai_reply = response['results'][0]['generated_text']
        
        # Add to cache if it's a common question (to reduce future costs)
        if len(user_message) < 50:  # Only cache shorter questions
            response_cache[user_message_lower] = ai_reply
        
        # Return the AI's reply as JSON
        return jsonify({"reply": ai_reply})
    except Exception as e:
        # Get user message for fallback responses
        data = request.get_json()
        user_message = data.get("message", "") if data else ""
        
        # Generic fallback
        fallback_response = f"I understand your question about '{user_message}'. As an AI assistant, I'd be happy to help, but I'm currently experiencing technical difficulties. Please try rephrasing your question or check back later. Error details: {str(e)}"
        return jsonify({"reply": fallback_response}), 200

@app.route("/dashboard")
def dashboard():
    pos = sentiments.count("Positive")
    neg = sentiments.count("Negative")
    neu = sentiments.count("Neutral")
    return render_template("dashboard.html", pos=pos, neg=neg, neu=neu, concerns=concerns)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Simple authentication - in production, use proper user validation
        if username == "admin" and password == "admin":
            session["user"] = username
            return redirect(url_for("chat"))  # Redirect to chat page
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
