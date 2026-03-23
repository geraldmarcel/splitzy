FROM python:3.9-slim

# Install library sistem untuk OpenCV dan PaddleOCR
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy semua file dari root ke dalam container
COPY . .

# Install library Python
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan FastAPI di port 7860 (standar Hugging Face)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
