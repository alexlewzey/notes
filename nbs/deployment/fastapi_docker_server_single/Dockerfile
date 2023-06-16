FROM python:3.10

COPY requirements.txt .

RUN pip install -r requirements.txt && \
     rm requirements.txt

COPY src ./src

COPY model ./model

EXPOSE 80

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "80"]
