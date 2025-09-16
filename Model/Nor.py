import typing
from .LogicComponent import LogicComponent

class Nor(LogicComponent):
	def eval(self) -> bool:
		"""Evaluate the NOR gate, and return if the Output has changed.

		Raises:
			ValueError: If the number of inputs is not exactly two.

		Returns:
			bool: True if the output state has changed, False otherwise.
		"""
		oldState = self.state["outValue"]
		if len(self.inputs) != 2:
			raise ValueError("NOR gate must have exactly two inputs.")
		# NOR logic: output True only if both inputs are False
		if not self.inputs[0].getState() and not self.inputs[1].getState():
			self.state["outValue"] = True
		else:
			self.state["outValue"] = False
		if self.state["outValue"] != oldState:
			return True
		else:
			return False
