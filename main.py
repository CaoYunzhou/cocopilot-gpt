import requests
from flask import Flask, request, Response, jsonify


app = Flask(__name__)


def forward_request(GHO_TOKEN: str, stream: bool, json_data):

    headers = {
        'Host': 'api.github.com',
        'authorization': f'token {GHO_TOKEN}',
        'editor-version': 'JetBrains-IU/232.10203.10',
        'editor-plugin-version': 'copilot-intellij/1.3.3.3572',
        'user-agent': 'GithubCopilot/1.129.0',
        'accept': '*/*',
    }

    response = requests.get(
        'https://api.github.com/copilot_internal/v2/token', headers=headers)
    # print("打印获取token的响应")
    # print(response.text)
    if response.status_code == 200:
        if response.json():
            access_token = response.json()['token']

            acc_headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
                'Editor-Version': 'vscode/1.83.1',
            }
            print(json_data)
            resp = requests.post(
                'https://api.githubcopilot.com/chat/completions', headers=acc_headers, json=json_data, stream=stream)
            print(response.text)
            return resp.iter_content(chunk_size=8192) if stream else resp.json()



@app.route('/v1/chat/completions', methods=['POST'])
def proxy():
    # 从请求中获取json数据
    json_data = request.get_json()
    if json_data is None:
        return "Request body is missing or not in JSON format", 400
    # 获取Authorization头部信息
    GHO_TOKEN = request.headers.get('Authorization')
    GHO_TOKEN = GHO_TOKEN.split(' ')[1]
    print("请求的秘钥", GHO_TOKEN)
    if GHO_TOKEN is None:
        return "Authorization header is missing", 401

    # Check if stream option is set in the request data
    stream = json_data.get('stream', False)

    # 转发请求并获取响应
    resp = forward_request(GHO_TOKEN, stream, json_data)
    return Response(resp, mimetype='application/json; charset=utf-8') if stream else resp


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
    app.run(host='0.0.0.0', port=8080, debug=True)


# GHO_TOKEN = "gho_xx"
# set_access_token(get_token(GHO_TOKEN)['token'])
