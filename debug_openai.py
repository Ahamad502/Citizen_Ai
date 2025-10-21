import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the OpenAI client from your app
from app import client

def test_openai_connection():
    print("Testing OpenAI connection...")
    print(f"API Key starts with: {client.api_key[:10]}...")
    
    try:
        # Simple test completion
        print("Sending test request to OpenAI...")
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Hello, this is a test message."}
            ],
            max_tokens=10
        )
        
        response_text = completion.choices[0].message.content
        print("Success! Received response:")
        print(response_text)
        return True
        
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        
        # Check for specific error types
        if "insufficient_quota" in str(e).lower():
            print("QUOTA ERROR: Your account has exceeded its current quota.")
        elif "invalid_api_key" in str(e).lower():
            print("AUTH ERROR: The API key is invalid or inactive.")
        elif "rate_limit" in str(e).lower():
            print("RATE LIMIT ERROR: Too many requests. Please wait before sending another request.")
        else:
            print("OTHER ERROR: An unexpected error occurred.")
            
        return False

if __name__ == "__main__":
    test_openai_connection()