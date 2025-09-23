import pytest
from src.model.EncoderEightBit import EncoderEightBit
from .DummyInput import DummyInput

def make_inputs(active_index):
    # Erzeuge 8 DummyInputs, nur einer ist True
    return [DummyInput(i == active_index) for i in range(8)]

@pytest.mark.parametrize("active, expected_bits", [
    (0, (0,0,0)),
    (1, (0,0,1)),
    (2, (0,1,0)),
    (3, (0,1,1)),
    (4, (1,0,0)),
    (5, (1,0,1)),
    (6, (1,1,0)),
    (7, (1,1,1)),
])
def test_encoder_eight_bit(active, expected_bits):
    encoder = EncoderEightBit()
    inputs = make_inputs(active)
    # Inputs an Encoder anschließen
    for i, inp in enumerate(inputs):
        encoder.addInput(inp, "outValue", f"input{i+1}")
    encoder.eval()
    # outValue3 = MSB, outValue2 = middle, outValue1 = LSB
    assert encoder.state["outValue3"][0] == expected_bits[0], f"MSB falsch für Input {active+1}"
    assert encoder.state["outValue2"][0] == expected_bits[1], f"Middle Bit falsch für Input {active+1}"
    assert encoder.state["outValue1"][0] == expected_bits[2], f"LSB falsch für Input {active+1}"
