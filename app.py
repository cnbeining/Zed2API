import os
from flask import Flask, request, Response
import requests
import json
import random
from helper import create_jwt, github_username_zed_userid_list

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    # Get the payload from the request
    payload = request.json

    # Get the model from the payload, defaulting to "claude-3-5-sonnet-20240620"
    model = payload.get('model', 'claude-3-5-sonnet-20240620')

    # Prepare the request for the LLM API
    url = "https://llm.zed.dev/completion?"
    
    llm_payload = {
        "provider": "anthropic",
        "model": model,
        "provider_request": {
            "model": model,
            "max_tokens": 8192,  # dont dare to change this for now
            "temperature": payload.get('temperature', 0),
            "top_p": payload.get('top_p', 0.7),
            "messages": payload['messages'],
            "system": ""
        }
    }

    github_username, zed_user_id = random.choice(github_username_zed_userid_list)
    jwt = create_jwt(github_username, zed_user_id)

    headers = {
        'Host': 'llm.zed.dev',
        'accept': '*/*',
        'content-type': 'application/json',
        'authorization': f'Bearer {jwt}',
        'user-agent': 'Zed/0.149.3 (macos; aarch64)'
    }

    # Get proxy from environment variable
    proxy = os.environ.get('HTTP_PROXY', None)
    proxies = {'http': proxy, 'https': proxy} if proxy else None

    def generate():
        with requests.post(url, headers=headers, json=llm_payload, stream=True, proxies=proxies) as response:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk

    return Response(generate(), content_type='application/octet-stream')

if __name__ == '__main__':
    app.run(debug=True)