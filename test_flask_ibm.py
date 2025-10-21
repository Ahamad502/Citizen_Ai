from flask import Flask, request, jsonify
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

app = Flask(__name__)

# IBM watsonx credentials
API_KEY = "c7f6wBkqUmkmyfbA4gmQAYGOLbiqBBhwP2nzr7elWFIS"
PROJECT_ID = "7d3f943c-f7aa-449b-9a3c-883516123e62"
URL = "https://us-south.ml.cloud.ibm.com"  # Dallas region URL

# Connect to IBM watsonx
try:
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
    print("IBM Watsonx AI client initialized successfully!")
except Exception as e:
    print(f"IBM Watsonx AI initialization failed: {e}")
    ibm_client_available = False

@app.route("/chatbot", methods=["POST"])
def chatbot():
    if not ibm_client_available:
        return jsonify({"reply": "IBM Watsonx AI service is not available."}), 500
    
    try:
        # Get the JSON message from the frontend
        data = request.get_json()
        user_message = data.get("message", "") if data else ""
        
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
        
        # Return the AI's reply as JSON
        return jsonify({"reply": ai_reply})
    except Exception as e:
        # Generic fallback
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)