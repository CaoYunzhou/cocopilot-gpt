FROM python:3.7-alpine
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk add --no-cache musl-dev openssl-dev libffi-dev tzdata gcc ttf-dejavu
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
COPY . /app/
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080
CMD ["python3", "main.py"]
