import requests
import json

def chat_with_bot():
    print("CitizenAI Chatbot - Type 'quit' to exit")
    print("-" * 40)
    
    while True:
        # Get user input
        user_message = input("You: ")
        
        # Check if user wants to quit
        if user_message.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        # Send message to chatbot
        try:
            response = requests.post(
                'http://127.0.0.1:5001/chatbot',
                headers={'Content-Type': 'application/json'},
                data=json.dumps({'message': user_message})
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"AI: {data['reply']}")
            else:
                print(f"Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Error connecting to chatbot: {e}")
        
        print()  # Empty line for readability

if __name__ == "__main__":
    chat_with_bot()