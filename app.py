from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def index():
    return send_from_directory(".","index.html")
@app.route("/revised_essay", methods=["POST"])
def generate_revised_essay():
    data=request.get_json()

    original_essay = data['original_essay']
    IELTS_level = data['IELTS_level']

    prompt = f"please check the {original_essay} grammar and spelling and provide a revised version depending on the  IELTS_level : {IELTS_level}"

    response = requests.post(
    "https://api.deepseek.com/v1/chat/completions",
    headers={
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
    },

    json={
    "model": "deepseek-chat",
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
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port,debug=False)