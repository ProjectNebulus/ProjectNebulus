FROM python:3.10

LABEL org.opencontainers.image.source="https://github.com/ProjectNebulus/ProjectNebulus"

ENV \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.1.11 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.local/bin"

RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
  # Installing `poetry` package manager:
  # https://github.com/python-poetry/poetry
  && curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

COPY ./poetry.lock ./pyproject.toml /opt/app/

# install deps
RUN poetry install --no-interaction --no-ansi \
  && poetry run pip install -U pip \
  && rm -rf "$POETRY_CACHE_DIR"

COPY oldmain.py /opt/app/
COPY app/templates/ /opt/app/templates
COPY app/static/ /opt/app/static

EXPOSE 8080:8080

CMD ["python3", "main.py"]
