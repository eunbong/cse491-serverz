class Klassy(object):
	def __init__(self, n):
		self.n = n

	def __call__(self):
		return 5*self.n

k = Klassy(5)
print k()
