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
# Normalize URL (avoid trailing slash issues)
BASE_URL = URL.rstrip("/")

# Strip whitespace from PROJECT_ID to avoid format issues
if PROJECT_ID:
    PROJECT_ID = PROJECT_ID.strip()

# Check if credentials are available
ibm_client_available = bool(API_KEY and PROJECT_ID)

if ibm_client_available:
    print(f"✓ IBM Watsonx AI credentials loaded successfully")
    print(f"  Project ID: {PROJECT_ID} (length: {len(PROJECT_ID)})")
    print(f"  Region: {BASE_URL}")
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

# ---------- Helper utilities ----------
def get_iam_token():
    """Obtain IAM access token for IBM Cloud using the API key."""
    try:
        resp = requests.post(
            "https://iam.cloud.ibm.com/identity/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}",
            timeout=10,
        )
        if resp.status_code != 200:
            return None, {
                "stage": "token",
                "status": resp.status_code,
                "body": safe_text(resp.text),
            }
        return resp.json().get("access_token"), None
    except requests.Timeout:
        return None, {"stage": "token", "error": "timeout"}
    except Exception as e:
        return None, {"stage": "token", "error": str(e)}


def generate_with_watsonx(access_token: str, prompt: str):
    """Call watsonx.ai text generation REST API and return reply or error."""
    try:
        # Use IBM watsonx.ai text generation endpoint. Provide project_id in headers and body for compatibility.
        generation_url = f"{BASE_URL}/ml/v1/text/generation?version=2023-05-29"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            "X-Project-Id": PROJECT_ID,
            "X-WML-Project-ID": PROJECT_ID,
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
                "top_p": 1,
            },
            "project_id": PROJECT_ID,
        }
        print(f"Sending request to: {generation_url}")
        print(f"Project ID in payload: '{payload['project_id']}' (len: {len(payload['project_id'])})")
        resp = requests.post(generation_url, headers=headers, json=payload, timeout=30)
        if resp.status_code != 200:
            return None, {
                "stage": "generation",
                "status": resp.status_code,
                "body": safe_text(resp.text),
            }
        data = resp.json()
        if isinstance(data, dict) and data.get("results"):
            return data["results"][0].get("generated_text"), None
        return None, {"stage": "generation", "error": "empty results", "raw": data}
    except requests.Timeout:
        return None, {"stage": "generation", "error": "timeout"}
    except Exception as e:
        return None, {"stage": "generation", "error": str(e)}


def safe_text(text: str, limit: int = 500) -> str:
    """Trim overly long log strings and avoid leaking secrets."""
    if not text:
        return ""
    t = str(text)
    return (t[:limit] + "…") if len(t) > limit else t


# Health endpoint to quickly validate IBM connectivity in production
@app.route("/health/ibm")
def health_ibm():
    if not ibm_client_available:
        return jsonify({"ok": False, "reason": "missing_credentials"}), 200
    token, terr = get_iam_token()
    if terr:
        return jsonify({"ok": False, "stage": terr.get("stage"), "detail": terr}), 200
    # Minimal dry-run prompt
    reply, gerr = generate_with_watsonx(token, "Say 'pong' only.")
    if gerr:
        return jsonify({"ok": False, "stage": gerr.get("stage"), "detail": gerr}), 200
    return jsonify({"ok": True, "reply": reply}), 200


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
            print("Getting IAM token…")
            access_token, terr = get_iam_token()
            if terr or not access_token:
                print(f"Token error: {terr}")
                return jsonify({"reply": "Sorry, I'm having trouble authenticating with the AI service. Please try again later."}), 200

            prompt = (
                "You are a helpful assistant for a civic engagement platform called CitizenAI. "
                "Answer concisely and helpfully. User question: " + user_message
            )

            print("Sending request to IBM Watsonx AI…")
            ai_reply, gerr = generate_with_watsonx(access_token, prompt)
            if gerr or not ai_reply:
                print(f"Generation error: {gerr}")
                return jsonify({"reply": "Sorry, I'm having trouble generating a response. Please try again later."}), 200
            
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