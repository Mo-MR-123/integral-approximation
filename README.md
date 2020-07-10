**A Python script to approximate integrals using Simpsons Rule and Trapezoid Rule**

**Why even approximate integrals?**

_Approximation of integrals can come in handy when you don't know the integral function or the function might be too complex_ 
_to calculate the integral form. Also, if you are lazy to calculate the integral from of the function and want a quick approximation._

**Requirements:**

- Python version 3.7 or up (so all version that include `futures` package).

**How to use:**

1. Open terminal and make sure you are in folder where the script is located. 

2. Type `python approximateIntegral.py a b n` on the terminal

**NOTE:** 

Here `a` must be a float value and the _MIN_ value of the integral interval

`b` must be a float value and the _MAX_ value of the integral interval

`n` is the amount of data point samples used to approximate the integral 
(the higher n is, the more accurate the approximation, the slower the calculation)

**TODO LIST:**

_Parallelize the approximation process for faster result_