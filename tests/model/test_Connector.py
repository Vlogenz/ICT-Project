import pytest
from src.model.Connector import Connector
from src.model.LogicComponent import LogicComponent

# Dummy LogicComponent for testing
class DummyLogicComponent(LogicComponent):
	def __init__(self, name=None, bitwidth=1, value=0):
		super().__init__()
		self.name = name
		self._state = {"outValue": (value, bitwidth)}
	def eval(self):
		return True
	def getState(self):
		return self._state

def test_connector_initial_state():
	c = Connector()
	assert c.getBitWidth() == 0
	assert c.getOrigin() is None
	assert c.getDestination() == []

def test_connector_set_and_get_state():
		# Connector no longer has setState/getState
		pass

def test_connector_set_and_get_origin():
	c = Connector()
	origin = DummyLogicComponent("origin", bitwidth=4)
	# bitWidth not set, should accept
	c.setOrigin(origin, "outValue")
	assert c.getOrigin() is origin
	assert c.getBitWidth() == 4
	# Try with mismatched bitWidth
	c2 = Connector()
	origin2 = DummyLogicComponent("origin2", bitwidth=2)
	c2.setBitWidth(4)
	with pytest.raises(ValueError):
		c2.setOrigin(origin2, "outValue")

def test_connector_add_and_remove_destination():
	c = Connector()
	d1 = DummyLogicComponent("d1", bitwidth=3)
	d2 = DummyLogicComponent("d2", bitwidth=3)
	# bitWidth not set, should accept first
	c.addDestination(d1, "outValue")
	assert c.getBitWidth() == 3
	c.addDestination(d2, "outValue")
	assert d1 in c.getDestination()
	assert d2 in c.getDestination()
	# Try with mismatched bitWidth
	d3 = DummyLogicComponent("d3", bitwidth=2)
	with pytest.raises(ValueError):
		c.addDestination(d3, "outValue")
	c.removeDestination(d1)
	assert d1 not in c.getDestination()
	assert d2 in c.getDestination()

def test_connector_remove_destination_not_in_list():
	c = Connector()
	d1 = DummyLogicComponent("d1", bitwidth=1)
	# Should raise ValueError if not present
	with pytest.raises(ValueError):
		c.removeDestination(d1)
