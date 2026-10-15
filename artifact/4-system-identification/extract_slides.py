#!/usr/bin/env python3
"""Render source PDFs page by page; run from this guide's directory.
Install Python dependencies: python -m pip install pdf2image pillow
Install Poppler: brew install poppler (macOS), apt install poppler-utils (Debian).
Defaults follow exact filename order: PEM then SIM; output assets/ in cwd.
"""
import argparse
import json
from pathlib import Path
from pdf2image import convert_from_path, pdfinfo_from_path
ROOT = Path(__file__).resolve().parents[2]
DEFAULTS = [ROOT / 'notes/4-System Identification' / name for name in
            ['System Identification (PEM).pdf', 'System Identification (SIM).pdf']]
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdfs', nargs='*', type=Path, default=DEFAULTS)
    parser.add_argument('--dpi', type=int, default=130)
    args = parser.parse_args()
    assets = Path.cwd() / 'assets'
    assets.mkdir(exist_ok=True)
    manifest = []
    for pdf in args.pdfs:
        deck = 'PEM' if '(PEM)' in pdf.name else 'SIM'
        for page in range(1, pdfinfo_from_path(str(pdf))['Pages'] + 1):
            number = len(manifest) + 1
            filename = f'slide_{number:02d}.png'
            image = convert_from_path(str(pdf), dpi=args.dpi, first_page=page, last_page=page)[0]
            image.save(assets / filename)
            manifest.append({'image_number': number, 'image': f'./assets/{filename}',
                             'figure_id': f'slide-{number:02d}', 'deck': deck,
                             'pdf': str(pdf.relative_to(ROOT)) if pdf.is_relative_to(ROOT) else str(pdf),
                             'page': page, 'width': image.width, 'height': image.height})
            image.close()
    Path('sources.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Rendered {len(manifest)} pages to {assets}')
if __name__ == '__main__':
    main()
