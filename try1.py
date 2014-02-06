def f(n):
	return 3 * n

def g():
	return f

value = g()
print value(5)
