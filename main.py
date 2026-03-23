import os
import cv2
import uvicorn
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from paddleocr import PaddleOCR

app = FastAPI()

# Izinkan CORS agar API bisa diakses secara fleksibel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inisialisasi PaddleOCR
# Menggunakan 'en' (English) karena struk biasanya menggunakan karakter latin
# use_angle_cls=True membantu mendeteksi teks jika foto miring
ocr = PaddleOCR(use_angle_cls=True, lang='en')

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Fungsi untuk menampilkan file index.html saat URL Space dibuka"""
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "File index.html tidak ditemukan. Pastikan file ada di root repository."

@app.post("/scan")
async def scan_receipt(file: UploadFile = File(...)):
    """API Endpoint untuk menerima gambar dan mengembalikan teks hasil OCR"""
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Proses gambar dengan PaddleOCR
        result = ocr.ocr(img, cls=True)
        
        extracted_data = []
        if result and result[0]:
            for line in result[0]:
                text = line[1][0]
                confidence = line[1][1]
                extracted_data.append({
                    "text": text, 
                    "confidence": round(float(confidence), 2)
                })
                
        return {"results": extracted_data}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Port 7860 wajib digunakan untuk Hugging Face Spaces
    uvicorn.run(app, host="0.0.0.0", port=7860)
