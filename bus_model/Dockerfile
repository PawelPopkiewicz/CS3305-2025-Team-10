
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y libpq-dev build-essential

WORKDIR /bus_model

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=/bus_model/app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5002

# cronjob minutely running update_GTFS_Realtime.sh
RUN chmod +x /scripts/update_GTFS_Realtime.sh
RUN (crontab -l ; echo "* * * * * /scripts/update_GTFS_Realtime.sh") | crontab

RUN pip install gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5002", "app:app"]
