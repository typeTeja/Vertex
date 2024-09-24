from typing import Optional

from fastapi import FastAPI, File, UploadFile
import pdfplumber

app = FastAPI()


@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    # Abre o arquivo PDF
    with pdfplumber.open(file.file) as pdf:
        text = ""
        # Extrai o texto de cada página
        for page in pdf.pages:
            text += page.extract_text()

    return {"extracted_text": text}
