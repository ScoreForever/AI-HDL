// Two independent engine FSMs plus per-buffer lifetime tracking.
module double_buffer_ctrl(
 input wire clk,rstn,start,load_done,compute_done,
 output reg load_req, output reg [1:0] load_tile, output reg load_buf,
 output reg compute_req, output reg [1:0] compute_tile, output reg compute_buf,
 output reg busy,done);
 reg loading,computing;
 reg [1:0] next_load,next_compute;
 reg [1:0] occupied,ready;
 reg loading_n,computing_n,busy_n,done_n;
 reg [1:0] nl,nc,occ,rd;
 reg lr,cr;
 reg [1:0] lt,ct;
 reg lb,cb;
 always @* begin
  loading_n=loading;computing_n=computing;busy_n=busy;done_n=0;
  nl=next_load;nc=next_compute;occ=occupied;rd=ready;
  lr=0;cr=0;lt=load_tile;ct=compute_tile;lb=load_buf;cb=compute_buf;
  if(!busy) begin
   if(start) begin
    busy_n=1;loading_n=0;computing_n=0;
    nl=0;nc=0;occ=0;rd=0;
   end
  end else begin
   if(loading && load_done) begin
    loading_n=0; rd[load_buf]=1;
   end
   if(computing && compute_done) begin
    computing_n=0;occ[compute_buf]=0;rd[compute_buf]=0;
    if(compute_tile==2) begin busy_n=0;done_n=1;end
   end
   if(busy_n) begin
    // Previous request must be low to keep every request a distinct pulse.
    if(!loading_n && !load_req && nl<3 && !occ[nl[0]]) begin
     lr=1;lt=nl;lb=nl[0];loading_n=1;occ[nl[0]]=1;nl=nl+1'b1;
    end
    if(!computing_n && !compute_req && nc<3 && rd[nc[0]]) begin
     cr=1;ct=nc;cb=nc[0];computing_n=1;nc=nc+1'b1;
    end
   end
  end
 end
 always @(posedge clk or negedge rstn) begin
  if(!rstn) begin
   loading<=0;computing<=0;next_load<=0;next_compute<=0;
   occupied<=0;ready<=0;load_req<=0;compute_req<=0;
   load_tile<=0;load_buf<=0;compute_tile<=0;compute_buf<=0;busy<=0;done<=0;
  end else begin
   loading<=loading_n;computing<=computing_n;next_load<=nl;next_compute<=nc;
   occupied<=occ;ready<=rd;load_req<=lr;compute_req<=cr;
   load_tile<=lt;load_buf<=lb;compute_tile<=ct;compute_buf<=cb;
   busy<=busy_n;done<=done_n;
  end
 end
endmodule
