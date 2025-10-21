from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# IBM Watsonx AI imports - with error handling
try:
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
    ibm_watsonx_available = True
except ImportError as e:
    print(f"Warning: ibm-watsonx-ai package not installed: {e}")
    print("Install it with: pip install ibm-watsonx-ai")
    ibm_watsonx_available = False

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_secret_key_change_this")

# IBM watsonx credentials from environment variables
API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")
URL = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")

# Connect to IBM watsonx
ibm_client_available = False
model = None
if ibm_watsonx_available and API_KEY and PROJECT_ID:
    try:
        print("Initializing IBM Watsonx AI...")
        credentials = Credentials(
            api_key=API_KEY,
            url=URL
        )
        # Initialize the model with a supported model
        model = ModelInference(
            model_id="ibm/granite-3-8b-instruct",
            credentials=credentials,
            project_id=PROJECT_ID
        )
        ibm_client_available = True
        print("✓ IBM Watsonx AI initialized successfully")
    except KeyboardInterrupt:
        print("\n✗ IBM Watsonx AI initialization cancelled")
        ibm_client_available = False
    except Exception as e:
        print(f"✗ IBM Watsonx AI initialization failed: {e}")
        print("App will run without AI features")
        ibm_client_available = False
else:
    if not ibm_watsonx_available:
        print("✗ IBM Watsonx AI package not available")
    elif not API_KEY or not PROJECT_ID:
        print("✗ IBM Watsonx AI credentials not found in .env file")
        print("App will run with fallback responses")
    ibm_client_available = False

# Simple cache for common questions (to reduce API costs)
response_cache = {
    "hello": "Hello! I'm your CitizenAI assistant. How can I help you today?",
    "hi": "Hi there! I'm your CitizenAI assistant. What can I do for you?",
    "how are you": "I'm just a computer program, but I'm functioning well! How can I assist you today?",
    "what can you do": "I'm an AI assistant for CitizenAI, a civic engagement platform. I can help answer questions about civic services, community issues, and government processes.",
    "who are you": "I'm the CitizenAI assistant, here to help you with civic engagement and community-related questions."
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

# AI chatbot endpoint
@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        # Get the JSON message from the frontend
        data = request.get_json()
        user_message = data.get("message", "") if data else ""
        
        # Validate input
        if not user_message:
            return jsonify({"reply": "I didn't receive a message. Please try again."}), 400
        
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
        prompt = f"You are a helpful assistant for a civic engagement platform called CitizenAI. Answer concisely and helpfully. User question: {user_message}"
        response = model.generate(prompt=prompt, params={
            "decoding_method": "greedy",
            "max_new_tokens": 300,
            "min_new_tokens": 10,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 1
        })
        
        # Extract the AI's reply
        if 'results' in response and len(response['results']) > 0:
            ai_reply = response['results'][0]['generated_text']
        else:
            ai_reply = "I'm having trouble generating a response right now. Please try again later."
        
        # Add to cache if it's a common question (to reduce future costs)
        if len(user_message) < 50 and len(user_message) > 0:
            response_cache[user_message_lower] = ai_reply
        
        # Return the AI's reply as JSON
        return jsonify({"reply": ai_reply})
    except Exception as e:
        # Log the error for debugging
        print(f"Chatbot error: {str(e)}")
        
        # Generic fallback
        fallback_response = "I'm currently experiencing technical difficulties. Please try again later."
        return jsonify({"reply": fallback_response}), 200

if __name__ == "__main__":
    app.run(debug=True)