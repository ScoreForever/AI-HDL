#!/usr/bin/env python3
"""Build Chinese PDF and submission ZIP with an explicit allowlist."""
from pathlib import Path
import subprocess,zipfile,argparse,re,os
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--team',default='team01');a=p.parse_args()
if not re.fullmatch(r'team(?:[0-9]+|xx)',a.team):p.error('Use team07 or teamxx style group ID')
d=R/'dist';d.mkdir(exist_ok=True);b=R/'build/report';b.mkdir(parents=True,exist_ok=True)
env=os.environ.copy()
tex='/workspace/tools/tex-cjk/usr/share/texlive/texmf-dist/tex'
if Path(tex).exists():env['TEXINPUTS']=tex+'//:'+env.get('TEXINPUTS','')
header=b/'header.tex';header.write_text(r'\usepackage{float}'+chr(10)+r'\floatplacement{figure}{H}'+chr(10))
name='Lab1_Report_'+a.team
source=(R/'docs/Lab1_Report_team01.md').read_text().replace('team01',a.team)
md=b/(name+'.md');md.write_text(source)
subprocess.run(['pandoc',str(md),'--pdf-engine=xelatex','--include-in-header='+str(header),'-V','papersize=a4','--resource-path='+str(R/'docs'),'-V','CJKmainfont=Noto Serif CJK SC','-V','mainfont=DejaVu Serif','-V','monofont=DejaVu Sans Mono','-V','geometry:margin=22mm','-V','fontsize=10pt','-V','colorlinks=true','-o',str(d/(name+'.pdf'))],check=True,env=env)
allowed={
 'winograd':['input_transform.v','weight_transform.v','output_transform.v','winograd_1d.v'],
 'cordic':['cordic.v'], 'fsm':['double_buffer_ctrl.v'], 'winograd_2d':['winograd_2d.v']}
with zipfile.ZipFile(d/(name+'.zip'),'w',zipfile.ZIP_DEFLATED) as z:
 z.write(d/(name+'.pdf'),name+'.pdf')
 for task,files in allowed.items():
  for f in files:z.write(R/'lab1'/task/'src'/f,f'{task}/src/{f}')
with zipfile.ZipFile(d/(name+'.zip')) as z:
 assert len(z.namelist())==8 and z.testzip() is None
 print('Submission files:');print('\n'.join(z.namelist()))
print('Created:',d/(name+'.pdf'),d/(name+'.zip'))
