import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import client

try:
    # Test the OpenAI API directly
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for a civic engagement platform called CitizenAI."},
            {"role": "user", "content": "test"}
        ]
    )
    
    ai_reply = completion.choices[0].message.content
    print("Success! Response:", ai_reply)
    
except Exception as e:
    print("Error:", str(e))
    print("Error type:", type(e).__name__)