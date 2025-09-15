import pytest
from Model.Connector import Connector
from Model.LogicComponent import LogicComponent

# Dummy LogicComponent for testing
class DummyLogicComponent(LogicComponent):
	def __init__(self, name=None):
		super().__init__()
		self.name = name
	def eval(self):
		return True

def test_connector_initial_state():
	c = Connector()
	assert c.getState() is False
	assert c.getOrigin() is None
	assert c.getDestination() is None

def test_connector_set_and_get_state():
	c = Connector()
	c.setState(True)
	assert c.getState() is True
	c.setState(False)
	assert c.getState() is False

def test_connector_set_and_get_origin():
	c = Connector()
	origin = DummyLogicComponent("origin")
	c.setOrigin(origin)
	assert c.getOrigin() is origin

def test_connector_add_and_remove_destination():
	c = Connector()
	c.destination = []  # Ensure destination is a list
	d1 = DummyLogicComponent("d1")
	d2 = DummyLogicComponent("d2")
	c.addDestination(d1)
	c.addDestination(d2)
	assert d1 in c.getDestination()
	assert d2 in c.getDestination()
	c.removeDestination(d1)
	assert d1 not in c.getDestination()
	assert d2 in c.getDestination()

def test_connector_remove_destination_not_in_list():
	c = Connector()
	c.destination = []
	d1 = DummyLogicComponent("d1")
	# Should raise ValueError if not present
	with pytest.raises(ValueError):
		c.removeDestination(d1)
