from fastapi import FastAPI, UploadFile, File, HTTPException
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
import tempfile
import os

app = FastAPI(title="Marker PDF to Markdown API")

converter = PdfConverter(
    artifact_dict=create_model_dict(),
)

@app.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        rendered = converter(tmp_path)
        markdown, _, _ = text_from_rendered(rendered)
    finally:
        os.remove(tmp_path)

    return {"markdown": markdown}