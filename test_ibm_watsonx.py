from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

# IBM Cloud credentials (replace with your actual credentials)
api_key = "YOUR_IBM_API_KEY"
project_id = "YOUR_PROJECT_ID"
url = "YOUR_IBM_URL"

try:
    # Initialize credentials
    credentials = Credentials(
        api_key=api_key,
        url=url
    )
    
    # Initialize the model
    model = ModelInference(
        model_id="meta-llama/llama-3-70b-instruct",
        credentials=credentials,
        project_id=project_id
    )
    
    print("IBM Watsonx AI client initialized successfully!")
    
    # Test generation (this will fail without valid credentials, but we're just testing the setup)
    try:
        response = model.generate(prompt="Hello, how are you?", params={
            "decoding_method": "greedy",
            "max_new_tokens": 100
        })
        print("Generation test successful!")
        print("Response:", response)
    except Exception as e:
        print(f"Generation test failed (expected without valid credentials): {e}")
        
except Exception as e:
    print(f"IBM Watsonx AI initialization failed: {e}")