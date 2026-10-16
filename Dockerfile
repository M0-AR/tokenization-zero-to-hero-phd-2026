FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /work
COPY requirements.txt pyproject.toml ./
COPY src ./src
COPY experiments ./experiments
COPY benchmarks ./benchmarks
COPY tests ./tests
COPY scripts ./scripts
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install -e .
CMD ["python", "benchmarks/run_all.py"]
