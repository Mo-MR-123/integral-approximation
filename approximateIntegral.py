import sys
from math import sqrt
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import random

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


def calculate_simpsons_sum_concurrent(func, a, delta_x, n, start_batch, end_batch) -> float:
	"""
	Used to sum values in interval of given batch using Simpsons algorithm
	(this should only be used for concurrency calculation)

	:param func: the function that is used to approximate integral of
	:param a: min. x value of interval for which to approx. integral
	:param delta_x: constant used in algorithm
	:param n: total number of data points
	:param start_batch: min number of current batch
	:param end_batch: max number of current batch
	:return: summation result of the interval part [start_batch, end_batch] acquired from n
	"""

	res = 0

	for i in range(start_batch, end_batch + 1):
		curr_x_val = get_xi(a, i, delta_x)

		if i == n or i == 0:
			curr_y_val = func(curr_x_val)
		elif i % 2 == 0:
			curr_y_val = 2 * func(curr_x_val)
		else:
			curr_y_val = 4 * func(curr_x_val)

		res += curr_y_val

	return res


def calculate_trapezoid_sum_concurrent(func, a, delta_x, n, start_batch, end_batch) -> float:
	"""
	Used to sum values in interval of given batch using Trapezoid algorithm
	(this should only be used for concurrency calculation)

	:param func: the function that is used to approximate integral of
	:param a: min. x value of interval for which to approx. integral
	:param delta_x: constant used in algorithm
	:param n: total number of data points
	:param start_batch: min number of current batch
	:param end_batch: max number of current batch
	:return: summation result of the interval part [start_batch, end_batch] acquired from n
	"""
	res = 0

	for i in range(start_batch, end_batch + 1):
		curr_x_val = get_xi(a, i, delta_x)

		if i == n or i == 0:
			curr_y_val = func(curr_x_val)
		else:
			curr_y_val = 2 * func(curr_x_val)

		res += curr_y_val

	return res


def approximate_integral_concurrent(func, a: float, b: float, n: int, threshold=400000) -> float:
	"""
	This method does the same as "approximate_integral" method, but this method does the calculations concurrently
	which makes approximation for large number of n faster and efficient.

	Multiprocessing happens only when n >= threshold as it is not efficient to parallelize for small amount of n.

	NOTE: this means that threshold must be chosen in such a way that
	a significant speedup can be achieved when using concurrency instead of without concurrency

	NOTE 2.0: Some precision is lost in the result when using this method (after the 8th decimal number)

	:param func: the function that is used to approximate integral of
	:param a: min. x value of interval for which to approx. integral
	:param b: max. x value of interval for which to approx. intergal
	:param n: amount of data point samples used to approximate the integral
	:param threshold: the number from which the approximation without concurrency takes more than 0 seconds to execute
	:return: float value of the approximation
	"""

	cpus_num = os.cpu_count()

	# if n < threshold, then just use original number as that is fast enough for small value of n
	if n < threshold:
		return approximate_integral(func, a, b, n)

	# calculate constants depending on whether n is even or not
	delta_x = calculate_delta_x(a, b, n)
	if n % 2 == 0:
		constant_num = delta_x / 3
	else:
		constant_num = delta_x / 2

	# divide the n into chunks equal to cpu's available on this pc
	# and create tuple batches intervals for concurrent calculation
	batch_per_cpu = []
	nums_in_one_batch = n // cpus_num

	for i in range(cpus_num):
		if i == 0:
			batch_per_cpu.append((0, nums_in_one_batch))
		elif cpus_num - 1 == i:
			# if n / cpus_num is not even number then to prevent missing numbers in calculations because of the rounding off
			# of the numbers in batch_per_cpu, then the remainder is the value that has been lost because of it.
			# So just add it back to last element in batch_per_cpu when the loop reaches the last element.
			min_val, max_val = batch_per_cpu[-1]
			min_val_curr_batch = max_val + 1
			max_val_curr_batch = max_val + nums_in_one_batch + (n % cpus_num)
			batch_per_cpu.append((min_val_curr_batch, max_val_curr_batch))
		else:
			# numbers in previous batch tuple in the list
			min_val, max_val = batch_per_cpu[-1]
			min_val_curr_batch = max_val + 1
			max_val_curr_batch = max_val + nums_in_one_batch
			batch_per_cpu.append((min_val_curr_batch, max_val_curr_batch))

	result = 0

	with ProcessPoolExecutor(max_workers=cpus_num) as executor:
		if n % 2 == 0:
			future_results = [executor.submit(calculate_simpsons_sum_concurrent, func, a, delta_x, n, start_batch, end_batch)
							  for (start_batch, end_batch) in batch_per_cpu]
		else:
			future_results = [executor.submit(calculate_trapezoid_sum_concurrent, func, a, delta_x, n, start_batch, end_batch)
							  for (start_batch, end_batch) in batch_per_cpu]

	for f in as_completed(future_results):
		result += f.result()

	return constant_num * result


if __name__ == '__main__':
	a = float(sys.argv[1])
	b = float(sys.argv[2])
	n = int(sys.argv[3])

	t1 = time.time()
	approx_val = approximate_integral_concurrent(function, a, b, n)
	t2 = time.time()

	print("APPROXIMATED RESULT: {}".format(approx_val))
	print("CALCULATION TOOK: {} SECONDS".format(t2 - t1))

	# BELOW CODE IF FOR TESTING PURPOSES ONLY
	# t1 = time.time()
	# approx_val = approximate_integral(function, a, b, n)
	# t2 = time.time()

	# t3 = time.time()
	# approx_val_concurrency = approximate_integral_concurrent(function, a, b, n)
	# t4 = time.time()

	# print("WITHOUT CONCURRENCY RESULT: {}".format(approx_val))
	# print("WITH CONCURRENCY RESULT: {}".format(approx_val_concurrency))
	# print("CALCULATION WITHOUT CONCURRENCY TOOK: {} SECONDS".format(t2 - t1))
	# print("CALCULATION WITH CONCURRENCY TOOK: {} SECONDS".format(t4 - t3))

