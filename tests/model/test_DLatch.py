import pytest
from src.model.DLatch import DLatch
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus

# Basic connection and state tests
def test_dlatch_initial_state():
    dlatch = DLatch()
    assert dlatch.state["outQ"] == (0,1)
    assert dlatch.state["out!Q"] == (1,1)
    assert dlatch.inputs["inputC"] is None
    assert dlatch.inputs["inputD"] is None

# Test output changes when clock is high
def test_dlatch_set_output_on_clock_high():
    getBus().setManual()
    dlatch = DLatch()
    clk = DummyInput(True)  # Clock high
    data = DummyInput(True) # Data high
    dlatch.addInput(clk, "outValue", "inputC")
    dlatch.addInput(data, "outValue", "inputD")
    changed = dlatch.eval()
    assert changed is True
    assert dlatch.state["outQ"] == (1,1)
    assert dlatch.state["out!Q"] == (0,1)

@pytest.mark.parametrize("clk, data, expected_q, expected_notq", [
    (False, False, 0, 1),
    (False, True, 0, 1),
    (True, False, 0, 1),
    (True, True, 1, 0),
])
def test_dlatch_parametrized(clk, data, expected_q, expected_notq):
    getBus().setManual()
    dlatch = DLatch()
    clk_in = DummyInput(clk)
    data_in = DummyInput(data)
    dlatch.addInput(clk_in, "outValue", "inputC")
    dlatch.addInput(data_in, "outValue", "inputD")
    dlatch.eval()
    assert dlatch.state["outQ"] == (expected_q,1)
    assert dlatch.state["out!Q"] == (expected_notq,1)

# Test output does not change when clock is low
def test_dlatch_no_change_on_clock_low():
    getBus().setManual()
    dlatch = DLatch()
    clk = DummyInput(False)  # Clock low
    data = DummyInput(True)  # Data high
    dlatch.addInput(clk, "outValue", "inputC")
    dlatch.addInput(data, "outValue", "inputD")
    changed = dlatch.eval()
    assert changed is False
    assert dlatch.state["outQ"] == (0,1)
    assert dlatch.state["out!Q"] == (1,1)

# Test output keeps previous value when clock goes low after being high
def test_dlatch_remembers_state_when_clock_goes_low():
    getBus().setManual()
    dlatch = DLatch()
    clk = DummyInput(True)
    data = DummyInput(True)
    dlatch.addInput(clk, "outValue", "inputC")
    dlatch.addInput(data, "outValue", "inputD")
    dlatch.eval()
    # Now set clock low, data low
    clk.setValue(False)
    data.setValue(False)
    changed = dlatch.eval()
    # Output should remain as previously set
    assert changed is False
    assert dlatch.state["outQ"] == (1,1)
    assert dlatch.state["out!Q"] == (0,1)
