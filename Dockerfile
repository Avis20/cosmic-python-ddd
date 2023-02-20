FROM python:3.10-alpine

RUN apk add curl htop postgresql-contrib

COPY ./pyproject.toml .
RUN pip install poetry
RUN poetry install

WORKDIR /src
COPY ./src /src
RUN pip install -e /src

ENV PYTHONPATH=.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

CMD ["poetry", "run", "python", "app/main.py"]
