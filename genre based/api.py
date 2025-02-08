import requests
import os
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API")

def get_genre_from_hf(song_name, artist, user_genre):
    prompt = f"Is the song '{song_name}' by '{artist}' a {user_genre} song? Give only 'YES' or 'NO' as output."

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 5}  # Ensure only YES or NO output
    }

    url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        return f"Error: {response.json().get('error', 'Unknown error')}"

    result = response.json()
    
    if not result:
        return "Error: No response from model"

    predicted_output = result[0]["generated_text"].strip().upper()
    yesORno=predicted_output.split()[len(predicted_output.split())-1]
    return "YES" if "YES" in yesORno else "NO"
