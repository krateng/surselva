FROM python:alpine

RUN \
	apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev && \
	pip install --no-cache-dir yt-dlp bottle waitress pyyaml jinja2 toml && \
	apk del .build-deps

RUN apk add ffmpeg

WORKDIR /usr/src/app
COPY . .

ENTRYPOINT ["python3","server.py","--ipv4","--datadir","/data"]
