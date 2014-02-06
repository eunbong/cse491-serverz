global_value = 6

def some_function(other_fn, value):
	value = value * global_value

	value2 = other_fn(value)

	return value2

def f(n):
	return n + 1

def g(m):
	return m - 1

print some_function(g, 5)
print some_function(f, 4)

global_value = 2

print some_function(g, 5)
print some_function(f, 4)
