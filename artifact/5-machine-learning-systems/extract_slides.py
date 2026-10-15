#!/usr/bin/env python3
"""Extract saved MATLAB figures and readable sources without running MATLAB.

Run from artifact/5-machine-learning-systems/: python extract_slides.py
No PDFs exist in this source folder. Defaults preserve the saved MLX figures.
Optional PDF mode: python extract_slides.py --pdf FILE.pdf [FILE.pdf ...]
Install pdf2image: uv run --with pdf2image python extract_slides.py --pdf FILE.pdf
Install Poppler: brew install poppler (macOS); apt install poppler-utils (Ubuntu).
PDF mode writes to assets/pdf/ to preserve the guide's source-figure mapping.
"""
import argparse
import base64
import io
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZipFile


def text_from_mlx(data):
    with ZipFile(io.BytesIO(data)) as archive:
        tree = ET.fromstring(archive.read('matlab/document.xml'))
        return '\n'.join(part for part in tree.itertext() if part.strip())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path)
    parser.add_argument('--pdf', nargs='+', type=Path)
    parser.add_argument('--dpi', type=int, default=150)
    args = parser.parse_args()
    if args.dpi <= 0:
        parser.error('--dpi must be positive')
    assets = Path.cwd() / 'assets'
    assets.mkdir(exist_ok=True)
    if args.pdf:
        from pdf2image import convert_from_path, pdfinfo_from_path
        target = assets / 'pdf'
        target.mkdir(exist_ok=True)
        number = 0
        for pdf in args.pdf:
            count = int(pdfinfo_from_path(str(pdf))['Pages'])
            for page in range(1, count + 1):
                images = convert_from_path(str(pdf), dpi=args.dpi, first_page=page, last_page=page)
                number += 1
                try:
                    images[0].save(target / f'slide_{number:02d}.png')
                finally:
                    for image in images:
                        image.close()
        print(f'Saved {number} PDF pages to {target}')
        return
    source = args.source_dir or Path(__file__).resolve().parents[2] / 'notes' / '5-Machine Learning Systems'
    text_dir = Path.cwd() / 'sources'
    text_dir.mkdir(exist_ok=True)
    manifest = []
    documents = [
        ('tree-ensemble', 'MachineLearningBasedIdentificationOfATwoTankSystemExample.mlx'),
        ('custom-regressors', 'Non Linear ARX  Two Tank Model.mlx'),
    ]
    bundles = [(label, name, (source / name).read_bytes()) for label, name in documents]
    with ZipFile(source / 'idnlbbdemo_siso.zip') as archive:
        bundles.append(('siso-tutorial', 'idnlbbdemo_siso.zip::idnlbbdemo_siso/idnlbbdemo_siso.mlx',
                        archive.read('idnlbbdemo_siso/idnlbbdemo_siso.mlx')))
        (text_dir / 'siso-tutorial.m').write_bytes(archive.read('idnlbbdemo_siso/idnlbbdemo_siso.m'))
        tank = archive.read('idnlbbdemo_siso/TwoTankBB.png')
    for label, name, data in bundles:
        (text_dir / f'{label}.txt').write_text(text_from_mlx(data))
        with ZipFile(io.BytesIO(data)) as archive:
            outputs = ET.fromstring(archive.read('matlab/output.xml'))
            for figure, element in enumerate(outputs.findall('.//figureUri'), 1):
                uri = element.text or ''
                if not uri.startswith('data:image/png;base64,'):
                    print(f'No saved PNG for {label}, figure {figure}; omitted placeholder.')
                    continue
                number = len(manifest) + 1
                image = f'slide_{number:02d}.png'
                (assets / image).write_bytes(base64.b64decode(uri.split(',', 1)[1], validate=True))
                manifest.append({'image': f'assets/{image}', 'source': name,
                                 'saved_figure': figure, 'label': label})
    image = f'slide_{len(manifest) + 1:02d}.png'
    (assets / image).write_bytes(tank)
    manifest.append({'image': f'assets/{image}',
                     'source': 'idnlbbdemo_siso.zip::idnlbbdemo_siso/TwoTankBB.png',
                     'label': 'two-tank-diagram'})
    (text_dir / 'evap_nl.m').write_bytes((source / 'evap_nl.m').read_bytes())
    (text_dir / 'relevant_links.md').write_bytes((source / 'relevant_links.md').read_bytes())
    Path('sources.json').write_text(json.dumps(manifest, indent=2))
    print(f'Extracted {len(manifest)} saved images and readable source text; MATLAB was not executed.')


if __name__ == '__main__':
    main()
