
FROM python:3.9-slim

WORKDIR /inference

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=/inference/app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5001

RUN pip install gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]
