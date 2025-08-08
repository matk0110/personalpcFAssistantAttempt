"""Lightweight OCR helper with optional portable Tesseract support.

Usage pattern (example):

    from src.receipt.ocr import extract_text
    text = extract_text("path/to/receipt.jpg")

Design goals:
 - Keep optional: if Tesseract binary or Pillow not present, raise a clear error.
 - Allow a portable (repo-local) install under tools/tesseract/tesseract.exe
 - Defer imports so normal non-OCR paths don't pay import cost.

To use a portable binary:
 - Place tesseract.exe at: <repo_root>/tools/tesseract/tesseract.exe
 - (Optional) language data (tessdata) alongside in tessdata/ folder.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List
import os

PORTABLE_TESSERACT = Path(__file__).resolve().parents[2] / "tools" / "tesseract" / "tesseract.exe"


class OCRError(RuntimeError):
    """Raised when OCR prerequisites are missing or processing fails."""


def _configure_tesseract() -> None:
    """Configure pytesseract to use a portable binary if available.

    Does nothing if pytesseract already finds a system-wide binary.
    """
    try:
        import pytesseract  # type: ignore

        # Allow explicit override via env var TESSERACT_CMD
        if "TESSERACT_CMD" in os.environ:
            pytesseract.pytesseract.tesseract_cmd = os.environ["TESSERACT_CMD"]
            return

        if PORTABLE_TESSERACT.exists():
            pytesseract.pytesseract.tesseract_cmd = str(PORTABLE_TESSERACT)
    except ImportError:
        pass  # Will be surfaced later on actual OCR call


def _assert_deps() -> None:
    missing: List[str] = []
    try:
        import PIL  # noqa: F401
    except Exception:
        missing.append("Pillow")
    try:
        import pytesseract  # noqa: F401
    except Exception:
        missing.append("pytesseract")
    if missing:
        raise OCRError(
            "Missing OCR dependencies: "
            + ", ".join(missing)
            + ". Install them or remove OCR usage."
        )

    # Verify binary availability
    import pytesseract  # type: ignore

    try:
        pytesseract.get_tesseract_version()
    except Exception as e:  # pragma: no cover
        raise OCRError(
            "Tesseract binary not found. Either install system-wide or place portable copy at "
            f"{PORTABLE_TESSERACT}. Original error: {e}"
        ) from e


def extract_text(image_path: str | Path, lang: str = "eng") -> str:
    """Extract raw text from an image file using Tesseract.

    Parameters
    ----------
    image_path : str | Path
        Path to image (jpg, png, etc.)
    lang : str
        Tesseract language code (default 'eng').
    """
    _configure_tesseract()
    _assert_deps()
    from PIL import Image  # defer heavy import
    import pytesseract  # type: ignore

    img = Image.open(image_path)
    return pytesseract.image_to_string(img, lang=lang)


def extract_lines(image_path: str | Path, lang: str = "eng") -> List[str]:
    """Extract text and return non-empty stripped lines."""
    text = extract_text(image_path, lang=lang)
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def bulk_extract(paths: Iterable[str | Path], lang: str = "eng") -> dict[str, List[str]]:
    """Process multiple image paths; return mapping path -> lines.

    Continues past individual failures, aggregating errors.
    """
    results: dict[str, List[str]] = {}
    errors: dict[str, str] = {}
    for p in paths:
        try:
            results[str(p)] = extract_lines(p, lang=lang)
        except Exception as e:  # pragma: no cover - simple passthrough
            errors[str(p)] = str(e)
    if errors:
        # Include partial success info
        raise OCRError(
            "Some OCR operations failed: " + "; ".join(f"{k}: {v}" for k, v in errors.items())
        )
    return results


__all__ = [
    "OCRError",
    "extract_text",
    "extract_lines",
    "bulk_extract",
]