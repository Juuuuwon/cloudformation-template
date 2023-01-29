FROM python:3.10-slim

RUN apt-get update
RUN apt-get install curl -y

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 80

CMD ["python", "main.py"]
