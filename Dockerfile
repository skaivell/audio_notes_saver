FROM python

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build deps, then runtime deps
COPY requirements.txt /app/requirements.txt

RUN pip install uv && uv init && uv sync

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev build-essential \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apt-get remove -y gcc build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
