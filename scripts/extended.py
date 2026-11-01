#!/usr/bin/env python3
"""Deterministic independent arithmetic tests and expanded public FSM timing driver."""
import pathlib,random,math,subprocess,os
R=pathlib.Path(__file__).resolve().parents[1];B=R/'build/extended';B.mkdir(parents=True,exist_ok=True)
iv=os.environ.get('IVERILOG','/workspace/tools/iverilog/usr/bin/iverilog');ivl=os.environ.get('IVL','/workspace/tools/iverilog/usr/lib/x86_64-linux-gnu/ivl');vvp=os.environ.get('VVP','/workspace/tools/iverilog/usr/bin/vvp')
rng=random.Random(20261101)
def signed(v):return v if v<2**31 else v-2**32
def value():return rng.choice([0,1,-1,2**31-1,-2**31]) if rng.random()<.35 else signed(rng.getrandbits(32))
def pack(a):return sum((v&0xffffffff)<<(32*i) for i,v in enumerate(a))
def run(name,source,rtl):
 f=B/(name+'.sv');f.write_text(source)
 c=subprocess.run([iv,'-B',ivl,'-g2012','-Wall','-s','tb','-o',str(B/name),str(f)]+[str(p) for p in rtl],text=True,capture_output=True);(B/(name+'.compile.log')).write_text(c.stdout+c.stderr);c.check_returncode()
 s=subprocess.run([vvp,str(B/name)],cwd=B,text=True,capture_output=True);(B/(name+'.log')).write_text(s.stdout+s.stderr);s.check_returncode();assert 'ALL PASS' in s.stdout;sout=s.stdout.strip();print(sout)
# Streaming 1D/2D: Python direct convolution is independent of RTL transforms.
for dim,count in [(1,2400),(2,1200)]:
 rows=[]
 for n in range(count):
  x=[value() for _ in range(4 if dim==1 else 16)];w=[value() for _ in range(3 if dim==1 else 9)]
  if dim==1:y=[sum(x[i+k]*w[k] for k in range(3)) for i in range(2)]
  else:y=[sum(x[(i+a)*4+j+b]*w[a*3+b] for a in range(3) for b in range(3)) for i in range(2) for j in range(2)]
  # Include bubbles, in-flight resets, and drain cycles.
  reset=int(n%211 not in (0,1));en=int(rng.random()<.8 and n<count-4)
  rows.append(f'{reset} {en} {pack(x):x} {pack(w):x} {pack(y):x}')
 (B/f'vectors{dim}.txt').write_text('\n'.join(rows)+'\n')
 nx,nw,ny=(128,96,64) if dim==1 else (512,288,128)
 if dim==1:
  inst='winograd_1d dut(clk,rstn,en,x[31:0],x[63:32],x[95:64],x[127:96],w[31:0],w[63:32],w[95:64],y[31:0],y[63:32],vld);'
  rtl=list((R/'lab1/winograd/src').glob('*.v'));rtl=[p for p in rtl if '_tb' not in p.name]
 else:inst='winograd_2d dut(clk,rstn,en,x,w,y,vld);';rtl=[R/'lab1/winograd_2d/src/winograd_2d.v']
 tb=f'''`timescale 1ns/1ps
module tb;
 reg clk=0;always #5 clk=~clk;
 reg rstn=0,en=0;reg [{nx-1}:0] x=0;reg [{nw-1}:0] w=0;
 wire [{ny-1}:0] y;wire vld;reg [{ny-1}:0] golden,q0,q1,q2;
 reg a0=0,a1=0,a2=0;integer fd,n=0,rc,rv,ev,checked=0;
 {inst}
 initial begin
  $dumpfile("stream{dim}.vcd");$dumpvars(0,tb);
  fd=$fopen("vectors{dim}.txt","r");
  while(!$feof(fd)) begin
   @(negedge clk); rc=$fscanf(fd,"%d %d %h %h %h\\n",rv,ev,x,w,golden);
   if(rc!=5) $fatal(1,"bad vector");rstn=rv;en=ev;
   @(posedge clk);
   if(!rstn) begin a0=0;a1=0;a2=0;q0=0;q1=0;q2=0;end
   else begin a2=a1;a1=a0;a0=en;q2=q1;q1=q0;q0=golden;end
   #1;
   if(vld!==a2) $fatal(1,"valid mismatch cycle %d",n);
   if(a2) begin if(y!==q2) $fatal(1,"arithmetic mismatch cycle %d expected %h got %h",n,q2,y);checked=checked+1;end
   if(!rstn && y!==0) $fatal(1,"reset output mismatch");n=n+1;
  end
  $display("ALL PASS: {dim}D streaming %0d cycles, %0d checked outputs",n,checked);$finish;
 end
endmodule
'''
 run(f'stream{dim}',tb,rtl)
# Full circle quarter-degree sweep plus arbitrary safe input vectors.
rows=[]
for i in range(1440+128):
 angle=i/4 if i<1440 else rng.random()*360
 x,y=(19432,0) if i<1440 else (rng.randrange(-9000,9001),rng.randrange(-9000,9001))
 z=round(angle/360*2**32)&0xffffffff;rad=z/2**32*2*math.pi
 gain=math.prod(math.sqrt(1+2**(-2*k)) for k in range(16))
 ex=round(gain*(x*math.cos(rad)-y*math.sin(rad)));ey=round(gain*(x*math.sin(rad)+y*math.cos(rad)))
 rows.append(f'{x} {y} {z:x} {ex} {ey}')
(B/'angles.txt').write_text('\n'.join(rows)+'\n')
run('angles','''`timescale 1ns/1ps
module tb;
 reg clk=0;always #2 clk=~clk;
 reg signed [15:0] x=0,y=0;reg [31:0] z=0;
 wire signed [15:0] xo,yo;wire done;
 integer fd,rc,ix,iy,ex,ey,dx,dy,n=0,maxerr=0;
 cordic dut(clk,x,y,z,xo,yo,done);
 initial begin
  fd=$fopen("angles.txt","r");
  while(!$feof(fd)) begin
   @(negedge clk);rc=$fscanf(fd,"%d %d %h %d %d\\n",ix,iy,z,ex,ey);
   if(rc!=5) $fatal(1,"bad vector");x=ix;y=iy;
   repeat(16) @(posedge clk);#1;
   if((^xo===1'bx)||(^yo===1'bx)||done!==1'b1) $fatal(1,"invalid cordic output");
   dx=xo-ex;dy=yo-ey;if(dx<0)dx=-dx;if(dy<0)dy=-dy;
   if(dx>maxerr)maxerr=dx;if(dy>maxerr)maxerr=dy;
   if(dx>8||dy>8) $fatal(1,"CORDIC mismatch angle=%h dx=%d dy=%d",z,dx,dy);n=n+1;
  end
  $display("ALL PASS: CORDIC %0d vectors, max absolute error %0d",n,maxerr);$finish;
 end
endmodule
''',[R/'lab1/cordic/src/cordic.v'])
# Keep every public scoreboard assertion; change only the supplemental driver.
fsm=(R/'lab1/fsm/src/double_buffer_ctrl_tb.sv').read_text()
start=fsm.index('    initial begin\n        run_case(3, 8);')
fsm=fsm[:start]+'''    initial begin
'''+''.join(f'        run_case({l}, {c});\n' for l in [1,2,3,5,8,13] for c in [1,2,3,5,8,13])+'''        reset_mid_job();
        $display("ALL PASS: FSM 36 latency pairs and active reset");
        $finish;
    end
endmodule
'''
fsm=fsm.replace('module double_buffer_ctrl_tb;','module tb;')
run('fsm_grid',fsm,[R/'lab1/fsm/src/double_buffer_ctrl.v'])
