FROM python:3.10

LABEL org.opencontainers.image.source="https://github.com/ProjectNebulus/ProjectNebulus"

ENV POETRY_VERSION=1.1.13
ENV PATH="$PATH:/root/.local/bin"

RUN curl -sSL 'https://install.python-poetry.org' | python - && poetry --version

WORKDIR /opt/nebulus/app
RUN poetry install

EXPOSE 8080:8080

ENTRYPOINT ["poetry", "run", "python3", "main.py"]
