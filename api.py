import requests
import os
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API")

def get_genre_from_hf(song_name, artist, user_genre):
    prompt = f"Identify the genre of the song '{song_name}' by '{artist}'. Only return the genre name."

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 20}
    }

    url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        return f"Error: {response.json().get('error', 'Unknown error')}"

    result = response.json()
    
    if not result:
        return "Error: No response from model"

    predicted_genre = result[0]["generated_text"].strip()

    return "Yes" if user_genre.lower() in predicted_genre.lower() else "No"

# 
# song_name = "humble"
# artist = "Kendrick Lamar"
# user_genre = "Rap"
# result = get_genre_from_hf(song_name, artist, user_genre)
# print(f"Does the song match the genre '{user_genre}'? {result}")
