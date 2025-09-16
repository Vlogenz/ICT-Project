import typing
from .LogicComponent import LogicComponent

class Xnor(LogicComponent):
	def eval(self) -> bool:
		"""Evaluate the XNOR gate, and return if the Output has changed.

		Raises:
			ValueError: If the number of inputs is not exactly two.

		Returns:
			bool: True if the output state has changed, False otherwise.
		"""
		oldState = self.state
		if len(self.inputs) != 2:
			raise ValueError("XNOR gate must have exactly two inputs.")
		# XNOR logic: output True if both inputs are the same
		a = self.inputs[0].getState()
		b = self.inputs[1].getState()
		self.state = (a == b)
		if self.state != oldState:
			return True
		else:
			return False
