__author__ = 'Alexander Prommesberger'
__matriclenumber__ = '03688679'
# git push https://gitlab.lrz.de/ga48rem/ams-lab.git
import math
import numpy
import scipy
import scipy.stats as st
import warnings
from copy import deepcopy

class Counter(object):
    """
    Counter class is an abstract class, that counts values for statistics.

    Values are added to the internal array. The class is able to generate mean value, variance and standard deviation.
    The report function prints a string with name of the counter, mean value and variance.
    All other methods have to be implemented in subclasses.
    """

    def __init__(self, name="default"):
        """
        Initialize a counter with a name.
        The name is only for better distinction between counters.
        :param name: identifier for better distinction between various counters
        """
        self.name = name
        self.values = []

    def count(self, *args):
        """
        Count values and add them to the internal array.
        Abstract method - implement in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def reset(self, *args):
        """
        Delete all values stored in internal array.
        """
        self.values = []

    def get_mean(self):
        """
        Returns the mean value of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def get_var(self):
        """
        Returns the variance of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def get_stddev(self):
        """
        Returns the standard deviation of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def report(self):
        """
        Print report for this counter.
        """
        if len(self.values) != 0:
            print('Name: ' + str(self.name) + ', Mean: ' + str(self.get_mean()) + ', Variance: ' + str(self.get_var()))

        else:
            print("List for creating report is empty. Please check.")


class TimeIndependentCounter(Counter):
    """
    Counter for counting values independent of their duration.

    As an extension, the class can report a confidence interval and check if a value lies within this interval.
    """

    def __init__(self, name="default"):
        """
        Initialize the TIC object.
        """
        super(TimeIndependentCounter, self).__init__(name)

    def count(self, *args):
        """
        Add a new value to the internal array. Parameters are chosen as *args because of the inheritance to the
        correlation counters.
        :param: *args is the value that should be added to the internal array
        """
        self.values.append(args[0])

    def get_mean(self):
        """
        Return the mean value of the internal array.
        """
        # TODO Task 2.3.1: Your code goes here
        return numpy.mean(self.values)

    def get_var(self):
        """
        Return the variance of the internal array.
        Note, that we take the estimated variance, not the exact variance.
        """
        # TODO Task 2.3.1: Your code goes here
        return numpy.sum(numpy.square(numpy.array(self.values) - numpy.mean(self.values))) / float(len(self.values) - 1)

    def get_stddev(self):
        """
        Return the standard deviation of the internal array.
        """
        # TODO Task 2.3.1: Your code goes here
        return numpy.sqrt(self.get_var())

    def report_confidence_interval(self, alpha=0.05, print_report=False):
        """
        Report a confidence interval with given significance level.
        This is done by using the t-table provided by scipy.
        :param alpha: is the significance level (default: 5%)
        :param print_report: enables an output string
        :return: half width of confidence interval h
        """
        # TODO Task 5.1.1: Your code goes here
        # https://www.statology.org/confidence-intervals-python/
        #st.t.ppf()
        #a, b = st.t.interval(1-alpha/2, df=len(self.values)-1, loc=self.get_mean())#, scale=st.sem(self.values)) # maybe scaling
        #mid_2 = (a+b)/2
        " I do not understand how the t test is different to these calculations"
        z = st.t.ppf(1-alpha/2, df=len(self.values)-1)
        mid = numpy.sqrt(self.get_var()/len(self.values))*z
        if print_report:
            print(f"{self.name}: Confidence interval: [{self.get_mean()-mid, self.get_mean()+mid}] ")
        return mid

    def is_in_confidence_interval(self, x, alpha=0.05):
        """
        Check if sample x is in confidence interval with given significance level.
        :param x: is the sample
        :param alpha: is the significance level
        :return: true, if sample is in confidence interval
        """
        # TODO Task 5.1.1: Your code goes here
        z = st.t.ppf(1-alpha/2, df=len(self.values)-1)
        mid = numpy.sqrt(self.get_var()/len(self.values))*z
        a, b = self.get_mean()-mid, self.get_mean()+mid
        return a < x < b

    def report_bootstrap_confidence_interval(self, alpha=0.05, resample_size=5000, print_report=True):
        """
        Report bootstrapping confidence interval with given significance level.
        This is done with the bootstrap method. Hint: use numpy.random.choice for resampling
        :param alpha: significance level
        :param resample_size: resampling size
        :param print_report: enables an output string
        :return: lower and upper bound of confidence interval
        """
        # TODO Task 5.1.2: Your code goes here
        #values_rs = numpy.random.choice(self.values, size=[len(self.values)])
        #while values_rs.size < len(self.values):
        means = []
        for _ in range(resample_size):
            values_rs = numpy.random.choice(self.values, size=[len(self.values)], replace=True)
            means.append(values_rs.mean())

        la, lb = int(alpha/2.0*resample_size), int((1-alpha/2.0)*resample_size)
        bootstramp_diff = numpy.array(means) - self.get_mean()
        a, b = self.get_mean()-numpy.sort(bootstramp_diff)[lb], self.get_mean()-numpy.sort(bootstramp_diff)[la]

        if print_report:
            print(f"{self.name}: Bootstramp Confidence interval: [{a, b}] ")
        return a, b

    def is_in_bootstrap_confidence_interval(self, x, resample_size=5000, alpha=0.05):
        """
        Check if sample x is in bootstrap confidence interval with given resample_size and significance level.
        :param x: is the sample
        :param resample_size: resample size
        :param alpha: is the significance level
        :return: true, if sample is in confidence interval
        """
        # TODO Task 5.1.2: Your code goes here
        a, b = self.report_bootstrap_confidence_interval(alpha=alpha, resample_size=resample_size, print_report=False)
        return a < x < b
        # if a < x < b:
        #     return True
        # else:
        #     return False


class TimeDependentCounter(Counter):
    """
    Counter, that counts values considering their duration as well.

    Methods for calculating mean, variance and standard deviation are available.
    """

    def __init__(self, sim, name="default"):
        """
        Initialize TDC with the simulation it belongs to and the name.
        :param: sim is needed for getting the current simulation time.
        :param: name is an identifier for better distinction between multiple counters.
        """
        super(TimeDependentCounter, self).__init__(name)
        self.sim = sim
        self.first_timestamp = 0
        self.last_timestamp = 0
        self.second_moment = []

    def count(self, value):
        """
        Adds new value to internal array.
        Duration from last to current value is considered.
        """
        # TODO Task 2.3.2: Your code goes here
        self.values.append(value*float(self.sim.sim_state.now-self.last_timestamp))
        self.second_moment.append((numpy.square(value)*float(self.sim.sim_state.now-self.last_timestamp)))
        self.last_timestamp = self.sim.sim_state.now

    def get_mean(self):
        """
        Return the mean value of the counter, normalized by the total duration of the simulation.
        """
        # TODO Task 2.3.2: Your code goes here
        return numpy.sum(self.values)/float(self.last_timestamp-self.first_timestamp)

    def get_var(self):
        """
        Return the variance of the TDC.
        """
        # TODO Task 2.3.2: Your code goes here
        second_moment_mean = (numpy.sum(self.second_moment)/float(self.last_timestamp-self.first_timestamp))
        return second_moment_mean-numpy.square(self.get_mean())
        # *(len(float(self.values)/float(self.values-1))) Why dont I need this n/n-1 like in lecuture ntoes?

    def get_stddev(self):
        """
        Return the standard deviation of the TDC.
        """
        # TODO Task 2.3.2: Your code goes here
        return numpy.sqrt(self.get_var())

    def reset(self):
        """
        Reset the counter to its initial state.
        """
        self.first_timestamp = self.sim.sim_state.now
        self.last_timestamp = self.sim.sim_state.now
        Counter.reset(self)


class TimeIndependentCrosscorrelationCounter(TimeIndependentCounter):
    """
    Counter that is able to calculate cross correlation (and covariance).
    """

    def __init__(self, name="default"):
        """
        Crosscorrelation counter contains three internal counters containing the variables
        :param name: is a string for better distinction between counters.
        """
        super(TimeIndependentCrosscorrelationCounter, self).__init__(name)
        # TODO Task 4.1.1: Your code goes here
        self.tic_1 = TimeIndependentCounter("Counter 1")
        self.tic_2 = TimeIndependentCounter("Counter 2")
        # I decided to not use a thrid counter even though the it could be used for Cov[X,Y] = E[XY] - E[X]E[Y] and this is an easier calculation than mine
        """Changed my mind, my previous method introduced a bias of 0.1 that was eliminated when I no longer divided 
        by n-1 but n! I do not understand why this is..."""
        self.tic_3 = TimeIndependentCounter("Counter 3")

    def reset(self):
        """
        Reset the TICCC to its initial state.
        """
        TimeIndependentCounter.reset(self)
        # TODO Task 4.1.1: Your code goes here
        self.tic_1.reset()
        self.tic_2.reset()
        self.tic_3.reset()

    def count(self, val_tic_1, val_tic_2):
        """
        Count two values for the correlation between them. They are added to the two internal arrays.
        """
        # TODO Task 4.1.1: Your code goes here
        self.tic_1.count(val_tic_1)
        self.tic_2.count(val_tic_2)
        self.tic_3.count(val_tic_2*val_tic_1)

    def get_cov(self):
        """
        Calculate the covariance between the two internal arrays x and y.
        :return: cross covariance
        """
        # TODO Task 4.1.1: Your code goes here
        """     
         arr_tic_1 = numpy.array(self.tic_1.values) - self.tic_1.get_mean()
         arr_tic_2 = numpy.array(self.tic_2.values) - self.tic_2.get_mean()
         return arr_tic_1.dot(arr_tic_2)/float(arr_tic_1.size)  #-1 dropped because it lead to test fail
         """
        return self.tic_3.get_mean()-self.tic_1.get_mean()*self.tic_2.get_mean()

    def get_cor(self):
        """
        Calculate the correlation between the two internal arrays x and y.
        :return: cross correlation
        """
        # TODO Task 4.1.1: Your code goes here
        # error in last tasks with different seeds
        if self.tic_1.get_var() != 0 and self.tic_2.get_var() != 0:
            return self.get_cov()/numpy.sqrt(self.tic_1.get_var()*self.tic_2.get_var())
        else:
            return 0

    def report(self):
        """
        Print a report string for the TICCC.
        """
        print('Name: ' + self.name + '; covariance = ' + str(self.get_cov()) + '; correlation = ' + str(self.get_cor()))


class TimeIndependentAutocorrelationCounter(TimeIndependentCounter):
    """
    Counter, that is able to calculate auto correlation with given max_lag.
    """

    def __init__(self, name="default", max_lag=10):
        """
        Create a new auto correlation counter object.
        :param name: string for better distinction between multiple counters
        :param max_lag: maximum available max_lag (defaults to 10)
        """
        super(TimeIndependentAutocorrelationCounter, self).__init__(name)
        # TODO Task 4.1.2: Your code goes here
        self.max_lag = max_lag
        #self.tic = TimeIndependentCounter(name)
        self.reset()

    def reset(self):
        """
        Reset the counter to its original state.
        """
        TimeIndependentCounter.reset(self)
        # TODO Task 4.1.2: Your code goes here
        #self.tic.reset()
        self.values = []

    def count(self, x):
        """
        Add new element x to counter.
        """
        # TODO Task 4.1.2: Your code goes here
        #self.tic.count(x)
        self.values.append(x)

    def get_auto_cov(self, lag):
        """
        Calculate the auto covariance for a given max_lag.
        :return: auto covariance
        """
        # TODO Task 4.1.2: Your code goes here
        if lag > self.max_lag:
            raise RuntimeError(f"The selected lag is grater than the max lag allowed! {lag}>{self.max_lag}")

        """
        This calculation had a problem. For a reason I do not fully understand, calculating the cov with the method 
        proposed in the lecture, a bias is introduced. If you instead reformulate the
        covariance to: Cov[X,Y] = E[XY] - E[X]E[Y], Y is shifted X, the problem is solved. I do not know why this is....
        arr_1 = numpy.array(self.tic.values) - self.tic.get_mean()  # numpy.array(self.tic.values[:-1*lag])  # much better implementation -1*lag! thx stack overflow!
        arr_2 = numpy.array(self.tic.values[-1*lag:] + self.tic.values[:-1*lag]) - numpy.mean(self.tic.values[-1*lag:] + self.tic.values[:-1*lag])  # numpy.array(self.tic.values[lag:])
        return arr_1.dot(arr_2) / (arr_1.size -1) # - 1 WTF!"""

        """What in the name of the lord is wrong with the lines -- finding this error cost me fucking 8h+ of my life and I still dont see the problem!"""
        # c_arr_base = numpy.array(deepcopy(self.values))#self.tic.values)
        # c_arr_cyc = numpy.array(deepcopy(self.values[-lag:]) + deepcopy(self.values[:-lag]))#self.tic.values[-1*lag:] + self.tic.values[:-1*lag])
        # c_arr_base_cyc_joint = numpy.array([a*b for a, b in zip(c_arr_base, c_arr_cyc)])
        #return numpy.mean(arr_base_cyc_joint) - numpy.mean(arr_base)*numpy.mean(arr_cyc)
        arr_base = self.values  # self.tic.values)
        arr_cyc = self.values[-lag:] + self.values[:-lag]
        arr_base_cyc_joint = [a*b for a, b in zip(arr_cyc, arr_base)]
        # diff = numpy.mean(c_arr_base_cyc_joint) - numpy.mean(c_arr_base)*numpy.mean(c_arr_cyc) \
        #        - (numpy.mean(arr_base_cyc_joint) - numpy.mean(arr_base)*numpy.mean(arr_cyc))
        # if diff != 0:
        #     pass
        ret =  numpy.mean(arr_base_cyc_joint) - numpy.mean(arr_base)*numpy.mean(arr_cyc) #deepcopy(numpy.mean(c_arr_base_cyc_joint) - numpy.mean(c_arr_base)*numpy.mean(c_arr_cyc))#deepcopy(numpy.mean(arr_base_cyc_joint) - numpy.mean(arr_base)*numpy.mean(arr_cyc))
        return ret

    def get_auto_cor(self, lag):
        """
        Calculate the auto correlation for a given max_lag.
        :return: auto correlation
        """
        # TODO Task 4.1.2: Your code goes here
        #var_1, var_2 = self.get_vars(lag)
        #return self.get_auto_cov(lag)/numpy.sqrt(var_1*var_2)
        if self.get_var() != 0:
            return self.get_auto_cov(lag)/self.get_var() #tic.get_var()
        else:
            return 0

        #return self.get_auto_cov(lag)/self.get_var() #tic.get_var()

    # def get_vars(self, lag):
    #     arr_1 = numpy.array(self.tic.values) - self.tic.get_mean()  # numpy.array(self.tic.values[:-1*lag])  # much better implementation -1*lag! thx stack overflow!
    #     arr_2 = numpy.array(self.tic.values[-1*lag:] + self.tic.values[:-1*lag]) - numpy.mean(self.tic.values[-1*lag:] + self.tic.values[:-1*lag])  # numpy.array(self.tic.values[lag:])
    #     var_1 = numpy.sum(numpy.square(arr_1)-numpy.mean(arr_1))/(arr_1.size-1)
    #     var_2 = numpy.sum(numpy.square(arr_2)-numpy.mean(arr_2))/(arr_2.size-1)
    #     return var_1, var_2

    def set_max_lag(self, max_lag):
        """
        Change maximum max_lag. Cycle length is set to max_lag + 1.
        """
        # TODO Task 4.1.2: Your code goes here
        self.max_lag = max_lag

    def report(self):
        """
        Print report for auto correlation counter.
        """
        print('Name: ' + self.name)
        for i in range(0, self.max_lag + 1):
            print('Lag = ' + str(i) + '; covariance = ' + str(self.get_auto_cov(i)) + '; correlation = ' + str(
                self.get_auto_cor(i)))

    def report_return(self):
        acc_list = []
        for i in range(0, self.max_lag + 1):
            acc_list.append(self.get_auto_cor(i))
        return acc_list
