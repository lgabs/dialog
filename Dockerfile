FROM python:3.11-slim

RUN pip install poetry==1.6.1

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY ./pyproject.toml ./README.md ./poetry.lock .

RUN poetry install --no-interaction --no-ansi --no-root

COPY ./src .
COPY /etc /app/etc
RUN chmod +x /app/etc/run.sh

EXPOSE 8080

ENV PYTHONPATH="/app:$PYTHONPATH"

CMD /app/etc/run.sh

