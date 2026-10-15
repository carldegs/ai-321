#!/usr/bin/env python3
"""Run from artifact/3-frequency-analysis/: python extract_slides.py [PDF ...] [--dpi 150].

Without PDF arguments, extracts all three notes/3-Frequency Analysis decks in the order used
by study_guide.html. Images are always written to ./assets/ in the current
working directory. Custom PDFs retain argument order and start at slide_01.
"""
# Install Python dependency: uv run --with pdf2image python extract_slides.py
# Install Poppler: macOS `brew install poppler`; Ubuntu `apt install poppler-utils`.
import argparse
import json
from pathlib import Path

from pdf2image import convert_from_path, pdfinfo_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdfs", nargs="*", type=Path, help="PDFs in slide-numbering order")
    parser.add_argument("--dpi", type=int, default=150, help="Image resolution (default: 150)")
    parser.add_argument("--poppler-path", type=str, help="Directory containing Poppler binaries")
    args = parser.parse_args()
    if args.dpi <= 0:
        parser.error("--dpi must be positive")
    review = Path(__file__).resolve().parent.parent.parent / "notes" / "3-Frequency Analysis"
    pdfs = args.pdfs or [
        review / "CT_FourierAnalysis .pdf",
        review / "DT_FourierAnalysis.pdf",
        review / "Intro_zTransforms.pdf",
    ]
    missing = [str(pdf) for pdf in pdfs if not pdf.is_file()]
    if missing:
        parser.error("PDF not found: " + ", ".join(missing))
    try:
        counts = [int(pdfinfo_from_path(str(pdf), poppler_path=args.poppler_path)["Pages"])
                  for pdf in pdfs]
    except (PDFInfoNotInstalledError, PDFPageCountError) as exc:
        parser.exit(1, f"Cannot inspect PDFs. Check Poppler installation and PDF validity: {exc}\n")
    assets = Path.cwd() / "assets"
    assets.mkdir(exist_ok=True)
    number = 0
    manifest = []
    try:
        for pdf, count in zip(pdfs, counts):
            for page in range(1, count + 1):
                images = convert_from_path(str(pdf), dpi=args.dpi, first_page=page,
                                           last_page=page, fmt="png",
                                           poppler_path=args.poppler_path)
                number += 1
                target = assets / f"slide_{number:02d}.png"
                try:
                    images[0].save(target, "PNG")
                finally:
                    for image in images:
                        image.close()
                manifest.append({"image_number": number, "image": f"./assets/{target.name}", "pdf": pdf.name, "page": page, "figure_id": f"slide-{number:02d}"})
                print(f"{target.name} <- {pdf.name}, page {page}")
    except Exception as exc:
        parser.exit(1, f"Extraction stopped after {number} pages: {exc}\n")
    Path("sources.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Saved {number} slides to {assets}")


if __name__ == "__main__":
    main()
