// F(2,3) input transform. Extend BEFORE arithmetic to preserve full range.
module input_transform(input signed [31:0] x0,x1,x2,x3,
 output signed [32:0] b0,b1,b2,b3);
 wire signed [32:0] a0={x0[31],x0}, a1={x1[31],x1};
 wire signed [32:0] a2={x2[31],x2}, a3={x3[31],x3};
 assign b0=a0-a2; assign b1=a1+a2;
 assign b2=a2-a1; assign b3=a1-a3;
endmodule
