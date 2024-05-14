/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_revenantx86_tinytpu 
(
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);
  //
  wire rst;
  wire data_in_x;
  wire data_in_y;
  wire load_en;
  wire init;
  wire data_out_z;
  wire tx_ready;
  //
  assign rst = ~rst_n;
  //
  /*
    Assign IO
  */
  // Input Assign
  ui_in[0] = data_in_x;
  ui_in[1] = data_in_y;
  ui_in[2] = load_en;
  ui_in[3] = init;
  
  // Output Assign
  uo_out[0] = data_out_z;
  uo_out[1] = tx_ready;
  uo_out[2] = 0;
  uo_out[3] = 0;
  uo_out[4] = 0;
  uo_out[5] = 0;
  uo_out[6] = 0;
  uo_out[7] = 0;
  
  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in
  assign uio_out = 0;
  assign uio_oe  = 0;
  

  tinytpu_top #(.D_W(8), .N(2), .WORD(4)) 
      tinytpu_top_inst (
                          .clk(clk),
                          .rst(rst),
                          .data_in_x(data_in_x),
                          .data_in_y(data_in_y),
                          .load_en(load_en),
                          .init(init),
                          .data_out_z(data_out_z),
                          .tx_ready(tx_ready)
                       );


endmodule
