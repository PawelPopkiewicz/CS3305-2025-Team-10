
FROM python:3.10-slim

WORKDIR /gateway

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENV FLASK_APP=/training_data_collection/app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# 
# EXPOSE 5000
# 
# RUN pip install gunicorn
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
