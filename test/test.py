# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
# Extra random library
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
import random

# Parameters
TEST_DURATION = 1000  # Test duration in simulation time units
D_W = 8
N = 2

  # data_in_x = ui_in[0];
  # data_in_y = ui_in[1];
  # load_en   = ui_in[2];
  # init      = ui_in[3];

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 40, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 40)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    #Load Data
    dut.ui_in[0].value <= 1; # Enable load
    for i in range(32):
        dut.ui_in[0].value <= random.randint(0, 1)  # data_in_x
        dut.ui_in[1].value <= random.randint(0, 1)  # data_in_y
        await Timer(40, units="ns")

    dut.ui_in[2].value <= 0  # De assert load
    await Timer(120, units="ns")  # Waiting period

    # Initialize
    dut.ui_in[3].value <= 1  # init
    await Timer(40, units="ns")
    dut.ui_in[3].value <= 0  # init

    bit_counter = 0
    index_counter = 0
    data = 0
    cc11 = 0
    cc12 = 0
    cc21 = 0
    cc22 = 0
    #

    # Wait for tx_ready to go high
    await RisingEdge(dut.tx_ready)
    cocotb.log.info("tx_ready is high, proceeding with test")

    await Timer(40, units="ns")  # Waiting period
    #
    for i in range(N*N*D_W*2):
        await RisingEdge(dut.clk)
        bit_counter += 1
        data = (int(dut.uo_out[0].value) << (2 * D_W - 1)) | (data >> 1)
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
        await Timer(40, units="ns")  # Waiting period
        #
        if bit_counter == (2 * D_W) - 1:
            index_counter += 1
        #

    await Timer(TEST_DURATION, units="ns")  # End simulation after a set duration
    
    # Wait for one clock cycle to see the output values
    #await ClockCycles(dut.clk, 1)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    #assert dut.uo_out.value == 50

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
