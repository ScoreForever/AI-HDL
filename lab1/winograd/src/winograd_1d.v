module winograd_1d(
 input wire clk,rstn,en,
 input wire signed [31:0] r1_x,r2_x,r3_x,r4_x,r1_w,r2_w,r3_w,
 output reg signed [31:0] r1_res,r2_res, output reg vld);
 wire signed [32:0] b0,b1,b2,b3;
 wire signed [33:0] g0,g1,g2,g3;
 reg signed [32:0] b0q,b1q,b2q,b3q;
 reg signed [33:0] g0q,g1q,g2q,g3q;
 reg signed [66:0] m0,m1,m2,m3;
 wire signed [31:0] y0,y1;
 reg v1,v2;
 input_transform it(r1_x,r2_x,r3_x,r4_x,b0,b1,b2,b3);
 weight_transform wt(r1_w,r2_w,r3_w,g0,g1,g2,g3);
 output_transform ot(m0,m1,m2,m3,y0,y1);
 always @(posedge clk or negedge rstn) begin
  if(!rstn) begin
   b0q<=0;b1q<=0;b2q<=0;b3q<=0;
   g0q<=0;g1q<=0;g2q<=0;g3q<=0;
   m0<=0;m1<=0;m2<=0;m3<=0;
   v1<=0;v2<=0;vld<=0;r1_res<=0;r2_res<=0;
  end else begin
   v1<=en;v2<=v1;vld<=v2;
   b0q<=b0;b1q<=b1;b2q<=b2;b3q<=b3;
   g0q<=g0;g1q<=g1;g2q<=g2;g3q<=g3;
   m0<=b0q*g0q;m1<=b1q*g1q;m2<=b2q*g2q;m3<=b3q*g3q;
   r1_res<=y0;r2_res<=y1;
  end
 end
endmodule
