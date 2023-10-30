# cocopilot
这个项目提供了一个快速简便的方式来使用cocopilot

## 建议自己部署
- 重点强调自己部署，降低风控

## 部署

- docker run快速开始：

```
  docker run -d \
  --name cocopilot-chatgpt \
  -p 8080:8080 \
  caoyunzhou/cocopilot-chatgpt
```

- [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/kQpQmc?referralCode=CG56Re)

## 使用

- IP访问
```
curl --location 'http://127.0.0.1:8080/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer gho_xxx' \
--data '{
  "model": "gpt-4",
  "messages": [{"role": "user", "content": "hi"}]
}'
```

- 域名访问
```
curl --location 'https://cocopilot.aivvm.com/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer gho_xxx' \
--data '{
  "model": "gpt-4",
  "messages": [{"role": "user", "content": "hi"}]
}'
```


## 获取cocopilot token GHO-xxx

[fakeopen by pengzhile](https://cocopilot.org/copilot/token)
