// Store 2*G*w: division by two is deferred until AFTER output summation.
module weight_transform(input signed [31:0] w0,w1,w2,
 output signed [33:0] g0,g1,g2,g3);
 wire signed [33:0] a={ {2{w0[31]}},w0};
 wire signed [33:0] b={ {2{w1[31]}},w1};
 wire signed [33:0] c={ {2{w2[31]}},w2};
 assign g0=a<<<1; assign g1=a+b+c;
 assign g2=a-b+c; assign g3=c<<<1;
endmodule
