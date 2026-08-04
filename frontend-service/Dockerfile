FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install \
    --no-cache-dir \
    -r requirements.txt

COPY app.py .
COPY templates ./templates

EXPOSE 5002

CMD ["python", "app.py"]