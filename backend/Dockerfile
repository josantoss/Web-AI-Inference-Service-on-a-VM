FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git procps && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
# Upgrade pip to latest to ensure modern resolver and wheel handling
RUN pip install --no-cache-dir --upgrade pip

# Install requirements. We use the official PyTorch CPU wheels to avoid
# pulling CUDA-enabled wheels (which are very large and may require
# platform-specific packages). The extra index URL points to the CPU
# build tags for the selected torch version.
RUN pip install --no-cache-dir --upgrade setuptools wheel && \
	pip install --no-cache-dir --prefer-binary \
		--extra-index-url https://download.pytorch.org/whl/cpu \
		-r requirements.txt
COPY . /app
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
