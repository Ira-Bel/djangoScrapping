FROM python:3.9

ENV PYTHONUNBUFRERED 1

WORKDIR /my_app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
