FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install flask openai pydantic

CMD ["python", "app.py"]