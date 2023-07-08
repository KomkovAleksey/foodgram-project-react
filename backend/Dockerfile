FROM python:3.11-slim
RUN echo 1
RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y libpq-dev gcc netcat-traditional

WORKDIR /app

COPY requirements.txt .
RUN pip install -U pip &&\
    pip install -r requirements.txt --no-cache-dir

COPY . .
RUN chmod +x run_app.sh
ENTRYPOINT ["bash","/app/run_app.sh"]
