FROM python:3.11-slim

LABEL maintainer="Team Sincryption"
LABEL version="2.0"
LABEL description="W0rm-GPT Educational CLI"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy rest of app
COPY . .

# Remove legacy compiled binary if present
RUN rm -f main.cpython-*.so __pycache__ -rf || true

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Default env
ENV OPENAI_API_KEY=""
ENV TERM=xterm-256color

ENTRYPOINT ["python3", "main.py"]
# For interactive: docker run -it --rm -e OPENAI_API_KEY=sk-... worm-gpt:2.0
