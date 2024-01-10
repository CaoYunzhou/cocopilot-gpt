# cocopilot

![GitHub repo size](https://img.shields.io/github/repo-size/caoyunzhou/cocopilot-gpt)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/caoyunzhou/cocopilot-chatgpt/latest)
![Docker Pulls](https://img.shields.io/docker/pulls/caoyunzhou/cocopilot-chatgpt)
[![GitHub Repo stars](https://img.shields.io/github/stars/caoyunzhou/cocopilot-gpt?style=social)](https://github.com/caoyunzhou/cocopilot-gpt/stargazers)

- 这个项目提供了一个快速简便的方式来使用cocopilot to chatgpt4
- `重点强调自己部署，降低风控`
- [[copilot](https://github.com/settings/copilot)](https://github.com/settings/copilot) 是一个免费的AI应用，让你可以和 GPT 模型聊天。让它可以通过一个 HTTP API 来访问，这个 API 模仿了官方的 OpenAI API for ChatGPT，所以它可以和其他使用 OpenAI API for ChatGPT 的程序兼容。

## 使用条件，获取copilot token GHO-xxx，GHU-xxx

- 你需要登录到github开通copilot的功能才能用
- 通过下面的地址便捷的获取 `GHO-xxx,GHU-xxx`
  - [fakeopen by pengzhile](https://cocopilot.org/copilot/token)

## 广告推广

- 使用企业github拼车copilot使用
- 低于官方**10$/月**: 可以联系QQ号：496618601

### Docker部署

- docker run快速开始：

```shell
  docker run -d \
  --name cocopilot-chatgpt \
  -p 8080:8080 \
  caoyunzhou/cocopilot-chatgpt
```

### Railway部署

- [注册Railway](https://railway.app?referralCode=CG56Re)
- [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/UhhP8o?referralCode=CG56Re)

### 使用方式

- IP访问

```shell
curl --location 'http://127.0.0.1:8080/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer gho_xxx' \
--data '{
  "model": "gpt-4",
  "messages": [{"role": "user", "content": "hi"}]
}'
```

- 域名访问

```shell
curl --location 'https://cocopilot.aivvm.com/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer gho_xxx' \
--data '{
  "model": "gpt-4",
  "messages": [{"role": "user", "content": "hi"}]
}'
```

- text-embedding-ada-002

```shell
curl --location 'https://cocopilot.aivvm.com/v1/embeddings' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer gho_xxx' \
--data '{
  "input":["Your text string goes here"],
  "model":"text-embedding-ada-002"
  }'
```

### 支持的模型

- gpt-4
- gpt-3.5-turbo
- text-davinci-003
- text-davinci-002
- text-davinci-001
- text-curie-001
- text-babbage-001
- text-ada-001
- davinci
- curie
- babbage
- ada
- code-davinci-002
- code-davinci-001
- code-cushman-002
- code-cushman-001
- davinci-codex
- cushman-codex
- text-davinci-edit-001
- code-davinci-edit-001
- text-embedding-ada-002
- text-similarity-davinci-001
- text-similarity-curie-001
- text-similarity-babbage-001
- text-similarity-ada-001
- text-search-davinci-doc-001
- text-search-curie-doc-001
- text-search-babbage-doc-001
- text-search-ada-doc-001
- code-search-babbage-code-001
- code-search-ada-code-001
- gpt2



### Star History

[![Star History Chart](https://api.star-history.com/svg?repos=caoyunzhou/cocopilot-gpt&type=Date)](https://star-history.com/#caoyunzhou/cocopilot-gpt&Date)
