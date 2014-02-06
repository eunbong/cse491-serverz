class Klassy(object):
	def __init__(self, n):
		self.n = n

	def val(self):
		def g(m):
			return 3 * self.n + m

		return g

k = Klassy(4)

fn = k.val()

k.n = 8
print fn(4)
