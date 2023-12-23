# packaging api into a docker image
FROM python:3.6.3-slim

LABEL maintaner="Alexander Lewzey a.lewzey@hotmail.co.uk" \
      description="Classify flower with tensorflow"

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip --no-cache-dir install -r /src/requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["app.py"]