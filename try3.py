class Klassy(object):
	def __init__(self, n):
		self.n = n
	
	def val(self):
		return 4*self.n

k = Klassy(5)
print k.val()
