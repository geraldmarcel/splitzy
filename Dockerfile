FROM python:3.9-slim

# Install library sistem yang dibutuhkan OpenCV dan PaddleOCR
# Kita ganti libgl1-mesa-glx menjadi libgl1
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy semua file ke dalam container
COPY . .

# Install library Python
RUN pip install --no-cache-dir -r requirements.txt

# Port 7860 untuk Hugging Face
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
