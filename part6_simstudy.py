__author__ = 'Alexander Prommesberger'
__matriclenumber__ = '03688679'
from statistictests import ChiSquare
import numpy as np

"""
This file should be used to keep all necessary code that is used for the verification section in part 6
of the programming assignment. It contains task 6.2.1.
"""


def task_6_2_1(n=100, bins=None, mean=0, var=1, alphas=None):
    """
    This task is used to verify the implementation of the chi square test.
    First, 100 samples are drawn from a normal distribution. Afterwards the chi square test is run on them to see,
    whether they follow the original or another given distribution.
    """
    # TODO Task 6.2.1: Your code goes here
    if alphas is None:
        alphas = [0.01, 0.05, 0.1]
    if bins is None:
        bins = np.sqrt(n).astype(np.int)
    values = [np.random.normal(loc=mean, scale=var) for _ in range(n)]

    emp_n, emp_x = np.histogram(values, bins=bins, range=(np.ceil(mean - 3 * var), np.ceil(mean + 3 * var)))
    cs = ChiSquare(emp_n=emp_n, emp_x=emp_x)

    for alpha in alphas:
        a, b = cs.test_distribution(alpha, 0, 1)
        print(f"For alpha={alpha} chi square returns: {a<b}")

if __name__ == '__main__':
    task_6_2_1()
