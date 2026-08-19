FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app.py db.py ./

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]