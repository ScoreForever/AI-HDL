#!/usr/bin/env python3
"""Run unmodified course TBs; NO_FSDB selects their supported portable mode."""
import os, subprocess, pathlib, re, json, hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
IV=os.environ.get('IVERILOG','/workspace/tools/iverilog/usr/bin/iverilog')
VVP=os.environ.get('VVP','/workspace/tools/iverilog/usr/bin/vvp')
IVL=os.environ.get('IVL','/workspace/tools/iverilog/usr/lib/x86_64-linux-gnu/ivl')
manifest=json.loads((ROOT/'docs/course_manifest.json').read_text())
for rel,digest in manifest['unmodified_files'].items():
 assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest, f'Course file changed: {rel}'
build=ROOT/'build'; build.mkdir(exist_ok=True)
checks=[('winograd','winograd_1d_tb',10),('cordic','cordic_tb',10),('fsm','double_buffer_ctrl_tb',3)]
for name,top,count in checks:
 src=ROOT/'lab1'/name/'src'; out=build/name;out.mkdir(exist_ok=True)
 # Separate root-only waveform module leaves course TB byte-for-byte unchanged.
 wave=out/'wave.v';wave.write_text(f'module wave; initial begin $dumpfile("wave.vcd"); $dumpvars(0,{top}); end endmodule\n')
 cmd=[IV,'-B',IVL,'-g2012','-Wall','-DNO_FSDB','-s',top,'-s','wave','-o',str(out/'simv')]+[str(p) for p in sorted(src.glob('*')) if p.suffix in ('.v','.sv')]+[str(wave)]
 comp=subprocess.run(cmd,cwd=out,text=True,capture_output=True);(out/'compile.log').write_text(comp.stdout+comp.stderr);comp.check_returncode()
 sim=subprocess.run([VVP,str(out/'simv')],cwd=out,text=True,capture_output=True);log=sim.stdout+sim.stderr;(out/'simulation.log').write_text(log);sim.check_returncode()
 passes=sum('PASS' in l and 'ALL PASS' not in l for l in log.splitlines())
 assert passes==count and 'ALL PASS' in log and not re.search(r'ERROR|FAIL|FATAL',log), log
 print(f'{name}: {passes} PASS; ALL PASS')
