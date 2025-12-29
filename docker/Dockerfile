# Dockerfile - PRSedm runner (minimal)
FROM python:3.10-slim

# system deps for pysam/bgzip/tabix etc
RUN apt-get update && \
    apt-get install -y build-essential gcc libbz2-dev liblzma-dev zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install PRSedm + GCS client
RUN pip install --no-cache-dir prsedm google-cloud-storage

# copy runner script
COPY runner.py /app/runner.py
RUN mkdir -p /data /output

ENTRYPOINT ["python","/app/runner.py"]