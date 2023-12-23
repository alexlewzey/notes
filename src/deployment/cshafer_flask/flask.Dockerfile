FROM python:3-alpine3.8

LABEL maintainer='Alexander Lewzey' \
        description='Web at to test docker'

WORKDIR /app

COPY requirements.txt /

RUN pip install --upgrade pip && \
    pip --no-cache-dir install -r /requirements.txt

EXPOSE 5000

VOLUME [ "/app" ]

ENTRYPOINT [ "python" ]

CMD [ "src/app.py" ]
