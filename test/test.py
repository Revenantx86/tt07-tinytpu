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
    bit_counter = 0
    index_counter = 0
    data = 0x0000
    cc11 = 0
    cc12 = 0
    cc21 = 0
    cc22 = 0
    #
    for i in range(0,64):
        #dut._log.info(f"bit counter: {bit_counter}")
        data = (data >> 1) | (int(dut.uo_out[0].value) << (2 * D_W - 1))
        #dut._log.info(f"data: {data:b}")
        #
        if index_counter == 0 and bit_counter == (2 * D_W) - 1:
            cc11 = data
        elif index_counter == 1 and bit_counter == (2 * D_W) - 1:
            cc12 = data
        elif index_counter == 2 and bit_counter == (2 * D_W) - 1:
            cc21 = data
        elif index_counter == 3 and bit_counter == (2 * D_W) - 1:
            cc22 = data
        #
        bit_counter += 1
        if bit_counter == (2 * D_W):
            index_counter += 1
            bit_counter = 0
        await Timer(40, units="ns")

    # Log the final value of resulting matrix
    dut._log.info(f"Final cc11 value: {cc11:#x}")
    dut._log.info(f"Final cc12 value: {cc12:#x}")
    dut._log.info(f"Final cc21 value: {cc21:#x}")
    dut._log.info(f"Final cc22 value: {cc22:#x}")
    await Timer(TEST_DURATION, units="ns")  # End simulation after a set duration

    assert cc11 == 0x2f91
    assert cc12 == 0x7625
    assert cc21 == 0x39f2
    assert cc22 == 0xae7c
    # Example assertion
    # assert dut.uo_out.value == expected_value

    # Continue testing as needed
