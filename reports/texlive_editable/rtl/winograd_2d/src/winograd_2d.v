// F(2x2,3x3). Flat element 0 occupies the least significant 32 bits.
// Separable transforms: V=B^T*d*B, U=(2G)*w*(2G)^T.
// U stores 4*G*w*G^T; divide by four only after A^T*(U.*V)*A.
module winograd_2d(input wire clk,rstn,en,
 input wire [511:0] x_flat, input wire [287:0] w_flat,
 output reg [127:0] res_flat, output reg vld);
 wire signed [31:0] d[0:15],w[0:8];
 wire signed [33:0] dt[0:15],v[0:15];
 wire signed [35:0] wt[0:11],u[0:15];
 reg signed [33:0] vq[0:15];
 reg signed [35:0] uq[0:15];
 reg signed [69:0] m[0:15];
 wire signed [73:0] mt[0:7],s[0:3];
 reg e1,e2;
 genvar r,c;
 generate
  for(r=0;r<16;r=r+1) begin: unpack_x
   assign d[r]=$signed(x_flat[32*r+:32]);
  end
  for(r=0;r<9;r=r+1) begin: unpack_w
   assign w[r]=$signed(w_flat[32*r+:32]);
  end
  for(c=0;c<4;c=c+1) begin: input_rows
   assign dt[c]=$signed(d[c])-$signed(d[8+c]);
   assign dt[4+c]=$signed(d[4+c])+$signed(d[8+c]);
   assign dt[8+c]=$signed(d[8+c])-$signed(d[4+c]);
   assign dt[12+c]=$signed(d[4+c])-$signed(d[12+c]);
  end
  for(r=0;r<4;r=r+1) begin: input_cols
   assign v[4*r]=dt[4*r]-dt[4*r+2];
   assign v[4*r+1]=dt[4*r+1]+dt[4*r+2];
   assign v[4*r+2]=dt[4*r+2]-dt[4*r+1];
   assign v[4*r+3]=dt[4*r+1]-dt[4*r+3];
  end
  for(c=0;c<3;c=c+1) begin: weight_rows
   assign wt[c]=$signed(w[c])*36'sd2;
   assign wt[3+c]=$signed(w[c])+$signed(w[3+c])+$signed(w[6+c]);
   assign wt[6+c]=$signed(w[c])-$signed(w[3+c])+$signed(w[6+c]);
   assign wt[9+c]=$signed(w[6+c])*36'sd2;
  end
  for(r=0;r<4;r=r+1) begin: weight_cols
   assign u[4*r]=wt[3*r]<<<1;
   assign u[4*r+1]=wt[3*r]+wt[3*r+1]+wt[3*r+2];
   assign u[4*r+2]=wt[3*r]-wt[3*r+1]+wt[3*r+2];
   assign u[4*r+3]=wt[3*r+2]<<<1;
  end
  for(c=0;c<4;c=c+1) begin: output_rows
   assign mt[c]=$signed(m[c])+$signed(m[4+c])+$signed(m[8+c]);
   assign mt[4+c]=$signed(m[4+c])-$signed(m[8+c])-$signed(m[12+c]);
  end
  for(r=0;r<2;r=r+1) begin: output_cols
   assign s[2*r]=mt[4*r]+mt[4*r+1]+mt[4*r+2];
   assign s[2*r+1]=mt[4*r+1]-mt[4*r+2]-mt[4*r+3];
  end
 endgenerate
 integer i;
 always @(posedge clk or negedge rstn) begin
  if(!rstn) begin
   e1<=0;e2<=0;vld<=0;res_flat<=0;
   for(i=0;i<16;i=i+1) begin vq[i]<=0;uq[i]<=0;m[i]<=0;end
  end else begin
   e1<=en;e2<=e1;vld<=e2;
   for(i=0;i<16;i=i+1) begin vq[i]<=v[i];uq[i]<=u[i];m[i]<=vq[i]*uq[i];end
   for(i=0;i<4;i=i+1) res_flat[32*i+:32]<=s[i][33:2];
  end
 end
endmodule
