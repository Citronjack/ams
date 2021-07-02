
from scipy import stats
import numpy as np


class ChiSquare(object):

    def __init__(self, emp_x, emp_n, name="default"):
        """
        Initialize chi square test with observations and their frequency.
        :param emp_x: observation values (bins)
        :param emp_n: frequency
        :param name: name for better distinction of tests
        """
        self.name = name
        # TODO Task 6.1.1: Your code goes here
        self.emp_x = emp_x
        self.emp_n = emp_n

    def test_distribution(self, alpha, mean, var):
        """
        Test, if the observations fit into a given distribution.
        :param alpha: significance of test
        :param mean: mean value of the gaussian distribution
        :param var: variance of the gaussian distribution
        """
        # TODO Task 6.1.1: Your code goes here
        g = stats.norm(loc=mean, scale=var)
        n_tot = np.sum(self.emp_n)
        self.trim_emp_xn(self.emp_x, self.emp_n)

        X2 = 0
        for i in range(len(self.emp_n)):
            e = (g.cdf(self.emp_x[i+1]) - g.cdf(self.emp_x[i]))*n_tot
            X2 += np.square(self.emp_n[i]-e)/e

        H1 = stats.chi2.ppf(1-alpha, df=len(self.emp_x)-1)

        return X2, H1

    def trim_emp_xn(self, emp_x, emp_n, t=5):
        n_add = 0
        idx_max = np.unravel_index(emp_n.argmax(), emp_n.shape)[0]
        idxs = [i for i in range(idx_max)] + [i for i in range(len(emp_n) - 1, idx_max, -1)]
        n_idxs_del = []
        x_idxs_del = []
        for i in idxs:
            if emp_n[i] < t:
                e = 1 if i < idx_max else -1
                emp_n[i + e] += emp_n[i]
                n_idxs_del.append(i)
                ee = 1 if i < idx_max else 0
                x_idxs_del.append(i + ee)

        self.emp_n = np.delete(emp_n, n_idxs_del)
        self.emp_x = np.delete(emp_x, x_idxs_del)
        return emp_x, emp_n
