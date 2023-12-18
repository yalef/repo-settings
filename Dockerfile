FROM python:3.11

RUN pip install poetry

WORKDIR .
COPY poetry.lock pyproject.toml .

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
COPY . .
CMD ["uvicorn", "src.api.app:app", "--reload"] 
