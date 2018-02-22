FROM gliderlabs/alpine:latest

COPY . /app
WORKDIR /app

RUN apk --update add --virtual build-deps python3-dev build-base linux-headers
RUN apk --update add python3 py3-pip openssl ca-certificates git \
    && pip3 install --upgrade setuptools \
    && pip3 install -r /app/requirements.txt && rm /app/requirements.txt \
    && apk del build-deps

EXPOSE 56567

CMD ["/usr/bin/python3", "/app/duh.py"]
