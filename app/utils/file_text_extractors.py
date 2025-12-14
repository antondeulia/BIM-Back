import mimetypes
from pathlib import Path

from pdfminer.high_level import extract_text
import pytesseract
from PIL import Image


def extract_text_from_file(path: str, content_type: str | None) -> str:
    ext = Path(path).suffix.lower()

    if ext == ".txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    if ext == ".pdf":
        return extract_text(path)

    if ext == ".docx":
        pass;

    if ext in {".png", ".jpg", ".jpeg", ".webp"}:
        image = Image.open(path)
        return pytesseract.image_to_string(image)

    raise ValueError(f"Unsupported file type: {ext}")
