import sys
from math import sqrt


def calculate_delta_x(a: float, b: float, n: int) -> float:
	"""
	Calculate delta_x = (b - a) / n
	n = data points samples
	a = min x value of integral
	b = max x value of intergal
	"""
	return (b - a) / n


def get_xi(a: float, i: int, delta_x: float) -> float:
	"""
	Calculating x_i = a + i * delta_x
	"""
	return a + (i * delta_x)


def function(x: float) -> float:
	"""
	The function of which the integral needs to be approximated
	NOTE: change function here if you want to approximate integral of another function 
	"""
	return 1 / sqrt(x + 1)


def calculate_trapezoidal(func, a: float, b: float, n: int) -> float:
	"""
	Using trapezoidal method to approximate integral of a given function
	
	:param: func: the function that is used to approximate integral of
	:param: a: min. x value of interval for which to approx. integral
	:param: b: max. x value of interval for which to approx. intergal
	:param: n: amount of data point samples used to approximate the integral
	:return: float value of the approximation
	"""
	
	delta_x = calculate_delta_x(a, b, n)

	# calculate delta_x / 2
	constant_num = delta_x / 2
	
	res = 0
	
	try:
		for i in range(n + 1):
			curr_x_val = get_xi(a, i, delta_x)

			if i == n or i == 0:
				curr_y_val = func(curr_x_val)
			else:
				curr_y_val = 2 * func(curr_x_val)
			
			res += curr_y_val
			
		return constant_num * res
		
	except KeyboardInterrupt:
		print("process interrupted. Last updated result: {}".format(constant_num * res))


def calculate_simpsons(func, a: float, b: float, n: int) -> float or str:
	"""
	Using Simpsons method to approximate integral of a given function
	NOTE: this method should only be used on EVEN NUMBER OF n

	:param: func: the function that is used to approximate integral of
	:param: a: min. x value of interval for which to approx. integral
	:param: b: max. x value of interval for which to approx. intergal
	:param: n: amount of data point samples used to approximate the integral (MUST BE EVEN NUMBER OF DATA POINTS)
	:return: float value of the approximation
	"""

	if n % 2 != 0:
		return "n must be an even number"

	delta_x = calculate_delta_x(a, b, n)

	# calculate delta_x / 3
	constant_num = delta_x / 3

	res = 0

	try:

		for i in range(n + 1):
			curr_x_val = get_xi(a, i, delta_x)

			if i == n or i == 0:
				curr_y_val = func(curr_x_val)
			elif i % 2 == 0:
				curr_y_val = 2 * func(curr_x_val)
			else:
				curr_y_val = 4 * func(curr_x_val)

			res += curr_y_val

		return constant_num * res

	except KeyboardInterrupt:
		print("process interrupted. Last updated result: {}".format(constant_num * res))


def approximate_integral(func, a: float, b: float, n: int) -> float:
	"""
	Main method to approximate integral. Depending on n, Simpsons or trapezoid method is used to calculate the integral.
	NOTE: the higher n is, the more accurate the approximation, the slower the calculation

	Approximate the integral from min. x value a to max. x value b of given function func
	provided n data point samples

	:param func: the function that is used to approximate integral of
	:param a: min. x value of interval for which to approx. integral
	:param b: max. x value of interval for which to approx. intergal
	:param n: amount of data point samples used to approximate the integral
	:return: float value of the approximation
	"""

	if n % 2 == 0:
		return calculate_simpsons(func, a, b, n)
	else:
		return calculate_trapezoidal(func, a, b, n)


if __name__ == '__main__':
	a = float(sys.argv[1])
	b = float(sys.argv[2])
	n = int(sys.argv[3])
	
	print(approximate_integral(function, a, b, n))
