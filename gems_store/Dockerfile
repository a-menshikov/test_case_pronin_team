FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY ./gems_store .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
