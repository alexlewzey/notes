uvicorn server:app --reload --host 0.0.0.0 --port 80

#docker run -p 80:80 --rm --name server-single penguin-server:single
#docker-compose up --build