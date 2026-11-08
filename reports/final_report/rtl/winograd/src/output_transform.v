module output_transform(input signed [66:0] m0,m1,m2,m3,
 output signed [31:0] y0,y1);
 wire signed [68:0] s0=$signed(m0)+$signed(m1)+$signed(m2);
 wire signed [68:0] s1=$signed(m1)-$signed(m2)-$signed(m3);
 // Sums are exactly even; select bits [32:1] = divide by 2, then low 32.
 assign y0=s0[32:1]; assign y1=s1[32:1];
endmodule
