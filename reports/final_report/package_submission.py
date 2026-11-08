from pathlib import Path
import zipfile
r=Path(__file__).resolve().parent
pdf=r/'Lab1_Report_team01.pdf'
files=sorted((r/'rtl').rglob('*.v'))
assert pdf.is_file() and len(files)==7
out=r/'submission';out.mkdir(exist_ok=True)
with zipfile.ZipFile(out/'Lab1_Report_team01.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.write(pdf,pdf.name)
 for f in files:z.write(f,str(f.relative_to(r/'rtl')))
print(out/'Lab1_Report_team01.zip')
