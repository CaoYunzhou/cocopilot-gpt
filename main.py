import requests
from flask import Flask, request, Response, jsonify
import uuid
import datetime
import hashlib
from os import environ

app = Flask(__name__)
machine_id = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
endpoint = environ.get('ENDPOINT', 'https://api.githubcopilot.com')
access = environ.get('TOKEN', '')


def get_header(access_token: str):
    return {
        'Authorization': f'Bearer {access_token}',
        'X-Request-Id': str(uuid.uuid4()),
        'Vscode-Sessionid': str(uuid.uuid4()) + str(int(datetime.datetime.utcnow().timestamp() * 1000)),
        'vscode-machineid': machine_id,
        'Editor-Version': 'vscode/1.84.2',
        'Editor-Plugin-Version': 'copilot-chat/0.10.2',
        'Openai-Organization': 'github-copilot',
        'Openai-Intent': 'conversation-panel',
        'Content-Type': 'application/json',
        'User-Agent': 'GitHubCopilotChat/0.10.2',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
    }


def forward_request(token: str, data, stream: bool = False):
    headers = {
        'Host': 'api.github.com',
        'authorization': f'token {token}',
        "Editor-Version": "vscode/1.84.2",
        "Editor-Plugin-Version": "copilot/1.138.0",
        "User-Agent": "GithubCopilot/1.138.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }

    preflight = requests.get(
        'https://api.github.com/copilot_internal/v2/token', headers=headers)
    print("Auth:", preflight.text)
    if preflight.status_code == 200 and preflight.json():
        access_token = preflight.json().get('token')

        resp = requests.post(
            endpoint + '/chat/completions',
            headers=get_header(access_token), json=data, stream=stream,
        )
        return resp
    else:
        return preflight


@app.route('/v1/chat/completions', methods=['POST'])
def proxy():
    data = request.get_json()
    if data is None:
        return "Request body is missing or not in JSON format", 400

    # get authorization token from request header (e.g. `gho_xxx` or Bearer `gho_xxx`)
    segment = request.headers.get('Authorization', access).split(' ')
    secret = segment[1] if len(segment) == 2 else segment[0]

    print("Secret:", secret)
    print("Message:", data)
    if secret is None:
        return "Authorization header is missing", 401

    # get stream flag from request body
    stream = data.get('stream', False)

    # forward request to copilot
    resp = forward_request(secret, data, stream)

    return (
        Response(generate_chunks(resp), content_type='text/event-stream')
        if stream else
        Response(resp.content, content_type='application/json')
    )


def generate_chunks(response):
    for chunk in response.iter_content(chunk_size=8192):
        try:
            yield chunk.decode('utf-8')
        except UnicodeDecodeError:
            # ignore invalid chunks
            pass


@app.route('/v1/models', methods=['GET'])
def models():
    data = {
        "object": "list",
        "data": [
            {"id": "gpt-4-0314", "object": "model", "created": 1687882410,
             "owned_by": "openai", "root": "gpt-4-0314", "parent": None},
            {"id": "gpt-4-0613", "object": "model", "created": 1686588896,
             "owned_by": "openai", "root": "gpt-4-0613", "parent": None},
            {"id": "gpt-4", "object": "model", "created": 1687882411,
             "owned_by": "openai", "root": "gpt-4", "parent": None},
            {"id": "gpt-3.5-turbo", "object": "model", "created": 1677610602,
             "owned_by": "openai", "root": "gpt-3.5-turbo", "parent": None},
            {"id": "gpt-3.5-turbo-0301", "object": "model", "created": 1677649963,
             "owned_by": "openai", "root": "gpt-3.5-turbo-0301", "parent": None},
        ]
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
