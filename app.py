from asgiref.wsgi import WsgiToAsgi
from flask import Flask, request, Response
import requests
import json
import random
from helper import create_jwt, get_github_username_zed_userid_list

app = Flask(__name__)

@app.route('/chat/completions', methods=['POST'])
async def chat():
    """
    Handle chat completion requests.

    This function processes incoming POST requests to the '/chat/completions' endpoint.
    It prepares the payload for the LLM API, generates a JWT for authentication,
    and streams the response from the LLM API back to the client.

    Returns:
        Response: A streaming response containing the LLM API's output.

    Note:
        - The function uses environment variables for proxy configuration.
        - It generates random GitHub username and Zed user ID for each request.
        - The LLM model defaults to "claude-3-5-sonnet-20240620" if not specified.
    """
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
            "max_tokens": payload.get('max_tokens', 8192),
            "temperature": payload.get('temperature', 0),
            "top_p": payload.get('top_p', 0.7),
            "messages": payload['messages'],
            "system": ""
        }
    }

    github_username, zed_user_id = get_github_username_zed_userid_list()
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

    async def generate():
        with requests.post(url, headers=headers, json=llm_payload, stream=True, proxies=proxies) as response:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk

    return Response(generate(), content_type='application/octet-stream')

# Convert the Flask app to an ASGI app
asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(asgi_app, host="0.0.0.0", port=8000)