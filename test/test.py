# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Timer
import random

# Parameters
TEST_DURATION = 1200  # Test duration in simulation time units
D_W = 8
N = 2

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 40 ns (25 MHz)
    clock = Clock(dut.clk, 40, units="ns")
    cocotb.start_soon(clock.start())

    data_x = 0xCA6C61EF  #goes x11x12x21x22 from LSB to MSB
    data_y = 0xC42F3B1B  #goes x11x12x21x22 from LSB to MSB

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 80) #wait 2 clock cycles
    dut.rst_n.value = 1

    # Load Sequence
    dut._log.info("Test project behavior")
    dut.ui_in[2].value = 1  # Enable load
    await Timer(60, units="ns") # Wait one clock cycle
    
    # Load Data
    for i in range(0,32): 
        #dut.ui_in[0].value = 1 
        dut.ui_in[0].value = (data_x >> i) & 1  # Get the i-th bit of data_x
        dut.ui_in[1].value = (data_y >> i) & 1  # Get the i-th bit of data_y
        await Timer(40, units="ns")
    
    #
    dut.ui_in[2].value = 0  # Deassert load
    await Timer(40, units="ns")  # Waiting period
    # Initialize
    dut.ui_in[3].value = 1  # init
    await Timer(40, units="ns")
    dut.ui_in[3].value = 0  # init
    await Timer(140, units="ns")
    # 
    # Example assertion
    # assert dut.uo_out.value == expected_value

    # Continue testing as needed
