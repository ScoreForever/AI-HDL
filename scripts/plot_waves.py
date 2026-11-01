#!/usr/bin/env python3
"""Render actual VCD traces, without reconstructing behavior from expected values."""
from pathlib import Path
import re,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/aihdl-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];OUT=R/'docs/figures';OUT.mkdir(parents=True,exist_ok=True)
def parse(path):
 scope=[];names={};traces={};header=True;t=0;scale=1
 lines=path.read_text().splitlines()
 for i,line in enumerate(lines):
  a=line.split()
  if not a:continue
  if header:
   if a[0]=='$timescale':
    raw=' '.join(a[1:]) if len(a)>1 else lines[i+1].strip()
    m=re.search(r'(\d+)\s*(ps|ns|us)',raw)
    if m:scale=int(m[1])*{'ps':.001,'ns':1,'us':1000}[m[2]]
   if a[0]=='$scope':scope.append(a[2])
   elif a[0]=='$upscope':scope.pop()
   elif a[0]=='$var':names['.'.join(scope+[a[4]])]=(a[3],int(a[2]));traces.setdefault(a[3],[])
   elif a[0]=='$enddefinitions':header=False
  elif line.startswith('#'):t=int(line[1:])*scale
  elif line.startswith('b'):
   v,code=a[0][1:],a[1]
   if code in traces:traces[code].append((t,v))
  elif line[0] in '01xz':
   code=line[1:]
   if code in traces:traces[code].append((t,line[0]))
 return names,traces

def plot(file,root,signals,lo,hi,name):
 names,traces=parse(file);fig,axes=plt.subplots(len(signals),1,figsize=(11,len(signals)*.55+1),sharex=True)
 for ax,signal in zip(axes,signals):
  signed=signal.startswith('~');signal=signal.lstrip('~');code,width=names[root+'.'+signal]
  data=traces[code];current='x';selected=[]
  for t,v in data:
   if t<=lo:current=v
   if lo<t<hi:selected.append((t,v))
  selected=[(lo,current)]+selected+[(hi,selected[-1][1] if selected else current)]
  if width==1:
   ax.step([t for t,v in selected],[int(v,2) if set(v)<=set('01') else .5 for t,v in selected],where='post',color='#2458a6');ax.set_ylim(-.2,1.3);ax.set_yticks([0,1]);ax.tick_params(axis='y',labelsize=7)
  else:
   ax.axhline(.5,color='#2458a6',lw=.8);ax.set_ylim(0,1);ax.set_yticks([])
   for j,(t,v) in enumerate(selected[:-1]):
    end=selected[j+1][0];ax.axvline(t,color='#2458a6',lw=.5)
    if end-t>(hi-lo)*.026:
     val=int(v,2) if set(v)<=set('01') else None
     if val is not None and signed and val>=2**(width-1):val-=2**width
     ax.text((t+end)/2,.5,str(val) if val is not None else v,ha='center',va='center',fontsize=7,bbox=dict(facecolor='white',edgecolor='none',pad=.3))
  ax.set_ylabel(signal,rotation=0,ha='right',va='center',fontsize=8);ax.grid(axis='x',alpha=.2);ax.spines[['top','right']].set_visible(False)
 axes[-1].set_xlim(lo,hi);axes[-1].set_xlabel('Time (ns)');fig.suptitle(name+' — actual Icarus VCD trace',fontsize=11);fig.tight_layout();fig.savefig(OUT/(name+'.png'),dpi=180);plt.close(fig)
plot(R/'build/winograd/wave.vcd','winograd_1d_tb',['clk','en','vld','~r1_res','~r2_res'],15,145,'winograd')
plot(R/'build/cordic/wave.vcd','cordic_tb',['clk','angle','~COSout','~SINout','done'],990,1080,'cordic')
plot(R/'build/fsm/wave.vcd','double_buffer_ctrl_tb',['clk','start','busy','load_req','load_tile','compute_req','compute_tile','load_active','compute_active','done'],30,450,'fsm')
