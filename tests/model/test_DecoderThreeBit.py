import pytest
from src.model.DecoderThreeBit import DecoderThreeBit
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus

@pytest.mark.parametrize("a, b, c,excepted", [
    (False,False,False,1),
    (False,False,True,2),
    (False,True,False,3),
    (False,True,True,4),
    (True,False,False,5),
    (True,False,True,6),
    (True,True,False,7),
    (True,True,True,8),
])
def test_decoder_three_bit_logic_state_and_change(a, b,c,excepted):
    getBus().setManual()
    decoder = DecoderThreeBit()
    decoder.addInput(DummyInput(a),"outValue","input1")
    decoder.addInput(DummyInput(b),"outValue","input2")
    decoder.addInput(DummyInput(c),"outValue","input3")
    changed = decoder.eval()
    assert decoder.state[f"outValue{excepted}"] == (1,1), f"DecoderThreeBit.state['outValue'] should be  after eval() with inputs {a}, {b}, {c}."
    assert changed is True, "DecoderThreeBit.eval() should return True if state changed from default."
    changed = decoder.eval()
    assert changed is False, "DecoderThreeBit.eval() should return False if state does not change."