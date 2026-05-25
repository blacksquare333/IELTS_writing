from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/revised_essay", methods=["POST"])
def generate_revised_essay():
    data=request.get_json()

    original_essay = data['original_essay']
    IELTS_level = data['IELTS_level']

    prompt = f"please check the {original_essay} grammar and spelling and provide a revised version depending on the  IELTS_level : {IELTS_level}"

    response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
    },

    json={
    "model": "anthropic/claude-3-haiku",
    "messages":[{"role": "user", "content": prompt}]
    }
)

    result=response.json()
  

    revised_essay = result['choices'][0]['message']['content']
    supabase_client.table("essay_logs").insert({
        "original_essay": original_essay,
        "IELTS_level": IELTS_level,
        "revised_essay": revised_essay
        }).execute()

    print(result)
    

    return jsonify({"revised_essay": revised_essay})



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=False)