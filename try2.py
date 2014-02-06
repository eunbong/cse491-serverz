def g(n):
	def f():
		return 8 * n
	
	return f

value = g(5)
print value()
