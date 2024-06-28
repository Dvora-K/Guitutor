FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirement.txt

COPY . .

CMD [ "python", "server.py" ]