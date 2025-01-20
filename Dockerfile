FROM ghcr.io/astral-sh/uv:python3.12-alpine

RUN apk add --no-cache ffmpeg

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY lib ./lib
RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

COPY . /app/src
WORKDIR /app/src

CMD ["python3", "-m", "bot"]
