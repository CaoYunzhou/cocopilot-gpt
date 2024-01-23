import requests
from flask import Flask, request, Response, jsonify
import uuid
import datetime
import hashlib

app = Flask(__name__)

machine_id = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()

def forward_request(GHO_TOKEN: str, stream: bool, json_data):

    headers = {
        'Host': 'api.github.com',
        'authorization': f'token {GHO_TOKEN}',
        'Editor-Version': 'vscode/1.85.2',
        'Editor-Plugin-Version': 'copilot-chat/0.11.1',
        'User-Agent': 'GitHubCopilotChat/0.11.1',
        'Accept': '*/*',
        "Accept-Encoding": "gzip, deflate, br"
    }

    response = requests.get(
        'https://api.github.com/copilot_internal/v2/token', headers=headers)
    print("Auth:",response.text)
    if response.status_code == 200 and response.json()['token']:
        access_token = response.json()['token']
        print("Requests_Token: %s" %(access_token))

        acc_headers = {
            'Host': 'api.githubcopilot.com',
            'Authorization': f'Bearer {access_token}',
            'X-Request-Id': str(uuid.uuid4()),
            'X-Github-Api-Version': '2023-07-07',
            'Vscode-Sessionid': str(uuid.uuid4()) + str(int(datetime.datetime.utcnow().timestamp() * 1000)),
            'vscode-machineid': machine_id,
            'Editor-Version': 'vscode/1.85.2',
            'Editor-Plugin-Version': 'copilot-chat/0.11.1',
            'Openai-Organization': 'github-copilot',
            'Copilot-Integration-Id': 'vscode-chat',
            'Openai-Intent': 'conversation-panel',
            'Content-Type': 'application/json',
            'User-Agent': 'GitHubCopilotChat/0.11.1',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        resp = requests.post('https://api.githubcopilot.com/chat/completions', headers=acc_headers, json=json_data, stream=stream)
        return resp.iter_content(chunk_size=8192) if stream else resp.json()
    else:
        # print(response.text)
        return response.json()


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
    resp = forward_request(GHO_TOKEN, stream, json_data)
    # 处理流式输出

    return Response(resp, mimetype='application/json') if stream else resp



def emb_forward_request(GHO_TOKEN: str, stream: bool, json_data):

    headers = {
        'Host': 'api.github.com',
        'authorization': f'token {GHO_TOKEN}',
        'Editor-Version': 'vscode/1.85.2',
        'Editor-Plugin-Version': 'copilot-chat/0.11.1',
        'User-Agent': 'GitHubCopilotChat/0.11.1',
        'Accept': '*/*',
        "Accept-Encoding": "gzip, deflate, br"
    }

    response = requests.get(
        'https://api.github.com/copilot_internal/v2/token', headers=headers)
    print("Auth:",response.text)
    if response.status_code == 200 and response.json()['token']:
        access_token = response.json()['token']
        print("Requests_Token: %s" %(access_token))

        acc_headers = {
            'Host': 'api.githubcopilot.com',
            'Authorization': f'Bearer {access_token}',
            'X-Request-Id': str(uuid.uuid4()),
            'X-Github-Api-Version': '2023-07-07',
            'Vscode-Sessionid': str(uuid.uuid4()) + str(int(datetime.datetime.utcnow().timestamp() * 1000)),
            'vscode-machineid': machine_id,
            'Editor-Version': 'vscode/1.85.2',
            'Editor-Plugin-Version': 'copilot-chat/0.11.1',
            'Openai-Organization': 'github-copilot',
            'Copilot-Integration-Id': 'vscode-chat',
            'Openai-Intent': 'conversation-panel',
            'Content-Type': 'application/json',
            'User-Agent': 'GitHubCopilotChat/0.11.1',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        resp = requests.post('https://api.githubcopilot.com/embeddings', headers=acc_headers, json=json_data, stream=stream)
        return resp.iter_content(chunk_size=8192) if stream else resp.json()
    else:
        # print(response.text)
        return response.json()


@app.route('/v1/embeddings', methods=['POST'])
def embeddings():
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
    resp = emb_forward_request(GHO_TOKEN, stream, json_data)
    # 处理流式输出

    return Response(resp, mimetype='application/json') if stream else resp


@app.route('/v1/models', methods=['GET'])
def models():
    data = {
        "object": "list",
        "data": [
            {"id": "text-search-babbage-doc-001","object": "model","created": 1651172509,"owned_by": "openai-dev"},
            {"id": "gpt-4-0613","object": "model","created": 1686588896,"owned_by": "openai"},
            {"id": "gpt-4", "object": "model", "created": 1687882411, "owned_by": "openai"},
            {"id": "babbage", "object": "model", "created": 1649358449, "owned_by": "openai"},
            {"id": "gpt-3.5-turbo-0613", "object": "model", "created": 1686587434, "owned_by": "openai"},
            {"id": "text-babbage-001", "object": "model", "created": 1649364043, "owned_by": "openai"},
            {"id": "gpt-3.5-turbo", "object": "model", "created": 1677610602, "owned_by": "openai"},
            {"id": "gpt-3.5-turbo-1106", "object": "model", "created": 1698959748, "owned_by": "system"},
            {"id": "curie-instruct-beta", "object": "model", "created": 1649364042, "owned_by": "openai"},
            {"id": "gpt-3.5-turbo-0301", "object": "model", "created": 1677649963, "owned_by": "openai"},
            {"id": "gpt-3.5-turbo-16k-0613", "object": "model", "created": 1685474247, "owned_by": "openai"},
            {"id": "text-embedding-ada-002", "object": "model", "created": 1671217299, "owned_by": "openai-internal"},
            {"id": "davinci-similarity", "object": "model", "created": 1651172509, "owned_by": "openai-dev"},
            {"id": "curie-similarity", "object": "model", "created": 1651172510, "owned_by": "openai-dev"},
            {"id": "babbage-search-document", "object": "model", "created": 1651172510, "owned_by": "openai-dev"},
            {"id": "curie-search-document", "object": "model", "created": 1651172508, "owned_by": "openai-dev"},
            {"id": "babbage-code-search-code", "object": "model", "created": 1651172509, "owned_by": "openai-dev"},
            {"id": "ada-code-search-text", "object": "model", "created": 1651172510, "owned_by": "openai-dev"},
            {"id": "text-search-curie-query-001", "object": "model", "created": 1651172509, "owned_by": "openai-dev"},
            {"id": "text-davinci-002", "object": "model", "created": 1649880484, "owned_by": "openai"},
            {"id": "ada", "object": "model", "created": 1649357491, "owned_by": "openai"},
            {"id": "text-ada-001", "object": "model", "created": 1649364042, "owned_by": "openai"},
            {"id": "ada-similarity", "object": "model", "created": 1651172507, "owned_by": "openai-dev"},
            {"id": "code-search-ada-code-001", "object": "model", "created": 1651172507, "owned_by": "openai-dev"},
            {"id": "text-similarity-ada-001", "object": "model", "created": 1651172505, "owned_by": "openai-dev"},
            {"id": "text-davinci-edit-001", "object": "model", "created": 1649809179, "owned_by": "openai"},
            {"id": "code-davinci-edit-001", "object": "model", "created": 1649880484, "owned_by": "openai"},
            {"id": "text-search-curie-doc-001", "object": "model", "created": 1651172509, "owned_by": "openai-dev"},
            {"id": "text-curie-001", "object": "model", "created": 1649364043, "owned_by": "openai"},
            {"id": "curie", "object": "model", "created": 1649359874, "owned_by": "openai"},
            {"id": "davinci", "object": "model", "created": 1649359874, "owned_by": "openai"},
            {"id": "gpt-4-0314", "object": "model", "created": 1687882410, "owned_by": "openai"}
        ]
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)


# GHO_TOKEN = "gho_xx"
# set_access_token(get_token(GHO_TOKEN)['token'])
