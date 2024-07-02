import os
from dotenv import load_dotenv

# # .envファイルの読み込み
load_dotenv()

import requests
import json

data = {
  "contents": [{
    "parts":[{
      "text": "こんにちは"
    }],
  }]
}
json_data = json.dumps(data)
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key=" + GOOGLE_API_KEY
# print(url)

response = requests.post(
    url,
    data=json_data,
    headers={"Content-Type": "application/json"}
)
# print(response.status_code)
result = response.json()
# print(response.json())  
result = result["candidates"][0]["content"]["parts"][0]["text"]

print(result)
