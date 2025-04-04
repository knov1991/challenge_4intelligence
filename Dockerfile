# Desafio 4 Intelligence

FROM python:3.11.7

WORKDIR /fastapi_notification

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /fastapi_notification

EXPOSE 8001

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
