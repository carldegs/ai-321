#!/usr/bin/env python3
"""Run from this output folder: python extract_slides.py [PDF ...].
Install: uv pip install pdf2image; macOS: brew install poppler;
Debian/Ubuntu: sudo apt install poppler-utils. Defaults preserve the guide's order.
Pages are rendered one at a time to bound peak memory; custom PDFs replace defaults.
"""
from pathlib import Path
import argparse, json
from pdf2image import convert_from_path, pdfinfo_from_path
NAMES = ['AI321_Curve fitting and Dynamic Systems.pdf','AI321_Lecture_Notes_SystemModels.pdf','Intro_Random_Process.pdf','LTI_system_representations.pdf','Overview of Time Series Analysis.pdf','Practice_problems_Sampling_and_Quantization.pdf','Review_DT_Signals_Systems.pdf','Review_System_Responses.pdf','Week 3 - MIMO.pdf','Week3_LTI_Systems_Analysis.pdf']
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pdfs',nargs='*',type=Path)
    ap.add_argument('--dpi',type=int,default=110)
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[2]/'notes'/'1-Analysis of LTI Systems and Review of Random Process'
    pdfs=args.pdfs or [root/n for n in NAMES]
    Path('assets').mkdir(exist_ok=True)
    manifest=[]
    for pdf in pdfs:
        count=pdfinfo_from_path(str(pdf))['Pages']
        for page in range(1,count+1):
            number=len(manifest)+1
            target=f'assets/slide_{number:02d}.png'
            img=convert_from_path(str(pdf),dpi=args.dpi,first_page=page,last_page=page)[0]
            img.save(target,optimize=True)
            manifest.append({'image_number':number,'image':target,'figure_id':f'slide-{number:02d}','pdf':pdf.name,'page':page,'width':img.width,'height':img.height})
        print(f'{pdf.name}: {count} pages',flush=True)
    Path('sources.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Rendered {len(manifest)} source pages.')
if __name__=='__main__': main()
