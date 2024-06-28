FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirement.txt

COPY . .

EXPOSE 5000

CMD [ "python", "server.py" ]