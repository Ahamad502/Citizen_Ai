from flask import Flask, render_template, jsonify, request
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_secret_key_change_this")

# IBM watsonx credentials from environment variables
API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")
URL = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")

# Check if credentials are available
ibm_client_available = bool(API_KEY and PROJECT_ID)

if ibm_client_available:
    print("✓ IBM Watsonx AI credentials loaded successfully")
else:
    print("✗ IBM Watsonx AI credentials not found")

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
        
        try:
            # Get IBM Cloud IAM token
            print(f"Getting IAM token...")
            token_response = requests.post(
                "https://iam.cloud.ibm.com/identity/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}",
                timeout=10
            )
            
            if token_response.status_code != 200:
                print(f"Token error ({token_response.status_code}): {token_response.text}")
                return jsonify({"reply": "Sorry, I'm having trouble authenticating with the AI service. Please try again later."}), 200
                
            access_token = token_response.json()["access_token"]
            print(f"✓ Token received successfully")
            
            # Send message to IBM Watsonx AI using REST API
            prompt = f"You are a helpful assistant for a civic engagement platform called CitizenAI. Answer concisely and helpfully. User question: {user_message}"
            
            generation_url = f"{URL}/ml/v1/text/generation?version=2023-05-29"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            payload = {
                "model_id": "ibm/granite-3-8b-instruct",
                "input": prompt,
                "parameters": {
                    "decoding_method": "greedy",
                    "max_new_tokens": 300,
                    "min_new_tokens": 10,
                    "temperature": 0.7,
                    "top_k": 50,
                    "top_p": 1
                },
                "project_id": PROJECT_ID
            }
            
            print(f"Sending request to IBM Watsonx AI...")
            response = requests.post(generation_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code != 200:
                print(f"Generation error ({response.status_code}): {response.text}")
                return jsonify({"reply": "Sorry, I'm having trouble generating a response. Please try again later."}), 200
            
            # Extract the AI's reply
            response_data = response.json()
            print(f"✓ Response received: {response_data}")
            
            if 'results' in response_data and len(response_data['results']) > 0:
                ai_reply = response_data['results'][0]['generated_text']
            else:
                ai_reply = "I'm having trouble generating a response right now. Please try again later."
            
            # Add to cache if it's a common question (to reduce future costs)
            if len(user_message) < 50 and len(user_message) > 0:
                response_cache[user_message_lower] = ai_reply
            
            # Return the AI's reply as JSON
            return jsonify({"reply": ai_reply})
            
        except requests.Timeout:
            print("Request timeout")
            return jsonify({"reply": "The AI service is taking too long to respond. Please try again."}), 200
        except Exception as api_error:
            print(f"API error: {str(api_error)}")
            return jsonify({"reply": "Sorry, I'm having trouble connecting to the AI service. Please try again later."}), 200
            
    except Exception as e:
        # Log the error for debugging
        print(f"Chatbot error: {str(e)}")
        
        # Generic fallback
        fallback_response = "I'm currently experiencing technical difficulties. Please try again later."
        return jsonify({"reply": fallback_response}), 200
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