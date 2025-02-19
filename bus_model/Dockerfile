
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y libpq-dev build-essential

RUN apt-get update && apt-get install -y dos2unix

WORKDIR /bus_model

COPY requirements.txt .
RUN dos2unix requirements.txt
RUN echo "pandas">>requirements.txt
RUN echo "psycopg">>requirements.txt
RUN echo "gunicorn">>requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENV FLASK_APP=/bus_model/app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# 
# EXPOSE 5002
# 
# RUN pip install gunicorn
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5002", "app:app"]
