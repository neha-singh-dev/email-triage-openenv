FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install flask openai pydantic openenv-core

CMD ["python", "server/app.py"]