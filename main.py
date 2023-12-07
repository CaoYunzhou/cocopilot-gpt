import requests
from flask import Flask, request, Response, jsonify
import uuid
import datetime
import hashlib

app = Flask(__name__)

machine_id = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()

def forward_request(GHO_TOKEN: str, json_data):

    headers = {
        'Host': 'api.github.com',
        'authorization': f'token {GHO_TOKEN}',
        "Editor-Version": "vscode/1.84.2",
        "Editor-Plugin-Version": "copilot/1.138.0",
        "User-Agent": "GithubCopilot/1.138.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }

    response = requests.get(
        'https://api.github.com/copilot_internal/v2/token', headers=headers)
    print("Auth:",response.text)
    if response.status_code == 200 and response.json():
        access_token = response.json()['token']

        acc_headers = {
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

        resp = requests.post('https://api.githubcopilot.com/chat/completions', headers=acc_headers, json=json_data, stream=False)
        return resp
    else:
        # print(response.text)
        return response


@app.route('/v1/chat/completions', methods=['POST'])
def proxy():
    # 从请求中获取json数据
    json_data = request.get_json()
    if json_data is None:
        return "Request body is missing or not in JSON format", 400
    # 获取Authorization头部信息
    GHO_TOKEN = request.headers.get('Authorization')
    GHO_TOKEN = GHO_TOKEN.split(' ')[1]
    print("Secret:", GHO_TOKEN)
    print("Message:", json_data)
    if GHO_TOKEN is None:
        return "Authorization header is missing", 401

    # Check if stream option is set in the request data
    stream = json_data.get('stream', False)

    # 转发请求并获取响应
    resp = forward_request(GHO_TOKEN, json_data)
    # 处理流式输出

    if stream:
        return Response(generate_chunks(resp), content_type='application/json')

    return Response(resp.content, content_type='application/json')

def generate_chunks(response):
    for chunk in response.iter_content(chunk_size=8192):
        yield chunk.decode('utf-8')


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


# GHO_TOKEN = "gho_xx"
# set_access_token(get_token(GHO_TOKEN)['token'])
