FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir openai pydantic

CMD ["python", "inference.py"]