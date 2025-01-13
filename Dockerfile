# Usando uma imagem oficial do Python
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update

COPY . /app/

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
