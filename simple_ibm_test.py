import requests
import json

# Test the IBM Watsonx AI integration directly
def test_ibm_watsonx():
    # IBM watsonx credentials
    API_KEY = "c7f6wBkqUmkmyfbA4gmQAYGOLbiqBBhwP2nzr7elWFIS"
    PROJECT_ID = "7d3f943c-f7aa-449b-9a3c-883516123e62"
    
    # Watsonx AI API endpoint
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # Payload
    payload = {
        "model_id": "ibm/granite-3-8b-instruct",
        "project_id": PROJECT_ID,
        "input": "Hello, how are you?",
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 100,
            "min_new_tokens": 10,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 1
        }
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            result = response.json()
            print("Success! Response:")
            print(result['results'][0]['generated_text'])
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_ibm_watsonx()