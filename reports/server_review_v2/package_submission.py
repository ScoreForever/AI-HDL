#!/usr/bin/env python3
"""Package only the reviewed PDF and seven implementation files."""
from pathlib import Path
import zipfile, subprocess, shutil
r=Path(__file__).resolve().parent
images=['summary','winograd-log','winograd-wave','cordic-log','cordic-wave','fsm-log','bonus-log']
missing=[f'server-{name}.png' for name in images if not (r/'figures'/f'server-{name}.png').exists()]
if missing:raise SystemExit('Missing original sanitized screenshots: '+', '.join(missing))
pdf=r/'Lab1_Report_team01.pdf'
if not shutil.which('pdftotext'):raise SystemExit('Install Poppler (pdftotext) to check PDF placeholders before packaging.')
text=subprocess.check_output(['pdftotext',str(pdf),'-'],text=True)
for marker in ['原图待嵌入','原图文件尚待提供','尚未进入文件系统','V2 待嵌图稿']:
 if marker in text:raise SystemExit('Update report status and rebuild PDF before packaging: '+marker)
files=sorted((r/'rtl').rglob('*.v'))
assert len(files)==7 and all('_tb' not in f.name for f in files)
out=r/'submission';out.mkdir(exist_ok=True)
with zipfile.ZipFile(out/'Lab1_Report_team01.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.write(pdf,pdf.name)
 for f in files:z.write(f,str(f.relative_to(r/'rtl')))
print(out/'Lab1_Report_team01.zip')
