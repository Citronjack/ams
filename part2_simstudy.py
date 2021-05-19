__author__ = 'Alexander Prommesberger'
__matriclenumber__ = '03688679'

from simulation import Simulation
from countercollection import *
from matplotlib import pyplot
import warnings, numpy

"""
This file should be used to keep all necessary code that is used for the simulation study in part 2 of the programming
assignment. It contains the tasks 2.7.1 and 2.7.2.

The function do_simulation_study() should be used to run the simulation routine, that is described in the assignment.
"""


class TaskCounterClass:

    def __init__(self, sim, plot_per_packet=False):
        self.mean_ql_counter = TimeIndependentCounter("Queue length")
        self.mean_wt_counter = TimeIndependentCounter("Waiting time")
        self.mean_ql_hist = TimeIndependentHistogram(sim, 'q')
        self.mean_wt_hist = TimeIndependentHistogram(sim, 'w')
        self.sim = sim
        self.wt_per_packet = []
        self.plot_per_packet = plot_per_packet

    def reset_all(self):
        self.mean_ql_counter.reset()
        self.mean_wt_counter.reset()
        self.mean_ql_hist.reset()
        self.mean_wt_hist.reset()

    def count_all(self, sim):
        self.mean_ql_counter.count(sim.counter_collection.cnt_ql.get_mean())
        self.mean_wt_counter.count(sim.counter_collection.cnt_wt.get_mean())

        # extra for waiting time per packet
        self.wt_per_packet.append(sim.counter_collection.cnt_ql.values)
        print(len(sim.counter_collection.cnt_ql.values))
        self.mean_ql_hist.count(sim.counter_collection.cnt_ql.get_mean())
        self.mean_wt_hist.count(sim.counter_collection.cnt_wt.get_mean())

    def report_all(self, sim):
        if not self.plot_per_packet:
            pyplot.figure(1)
            pyplot.subplot(2,1,1)
            self.mean_ql_hist.report()
            pyplot.title(f"Hist shows the mean Queue Length for {sim.sim_param.S_VALUES}")
            pyplot.xlabel("Queue size")
            pyplot.ylabel("approx. distribution")
            pyplot.subplot(2, 1, 2)

            self.mean_wt_hist.report()
            pyplot.title(f"Lineplot shows the mean waiting time for {sim.sim_param.S_VALUES}")
            pyplot.xlabel("Time in ms")
            pyplot.ylabel("approx. distribution")

            self.mean_ql_counter.report()
            self.mean_wt_counter.report()

        if sim.sim_param.S == 5 and self.plot_per_packet:
            self.report_mean_wt_per_packet()

    def report_mean_wt_per_packet(self):
        pyplot.figure(3)
        pyplot.title(f"Per packet waiting time for {self.sim.sim_param.SIM_TIME}")
        pyplot.xlabel("packet number")
        pyplot.ylabel("waiting time")
        """ TODO: """
        mx = 666
        for row in self.wt_per_packet:
            mx = len(row) if len(row) < mx else mx
        arr_tmp = numpy.zeros(mx)
        for row in self.wt_per_packet:
            arr_tmp += numpy.array(row[:mx])
        pyplot.plot(range(mx), arr_tmp/len(self.wt_per_packet))


def task_2_7_1(plot_per_packet=False):
    """
    Here, you should execute task 2.7.1 (and 2.7.2, if you want).
    """
    # TODO Task 2.7.1: Your code goes here
    sim = Simulation()
    sim.sim_param.S_VALUES = [5, 6, 7]
    cNh = TaskCounterClass(sim, plot_per_packet)

    for S_tmp in sim.sim_param.S_VALUES:

        sim.sim_param.NO_OF_RUNS = 1000
        sim.sim_param.SIM_TIME = 100 * 1000

        sim.sim_param.S = S_tmp
        cNh.reset_all()
        # sim.counter_collection.hist_wt.report()
        # sim.counter_collection.hist_ql.report()
        print("-----------------------------------------------")
        print(f"Gonna do a sim with paras - S:{sim.sim_param.S}")
        for i in range(sim.sim_param.NO_OF_RUNS):
            sim.reset()
            sim.do_simulation()
            cNh.count_all(sim)

        cNh.report_all(sim)

    pyplot.show()


def task_2_7_2(plot_per_packet=False):
    """
    Here, you can execute task 2.7.2 if you want to execute it in a separate function
    """
    # TODO Task 2.7.2: Your code goes here or in the function above
    sim = Simulation()
    sim.sim_param.S_VALUES = [5, 6, 7]
    cNh = TaskCounterClass(sim, plot_per_packet)

    for S_tmp in sim.sim_param.S_VALUES:

        sim.sim_param.NO_OF_RUNS = 1000
        sim.sim_param.SIM_TIME = 100 * 10000

        sim.sim_param.S = S_tmp
        cNh.reset_all()
        # sim.counter_collection.hist_wt.report()
        # sim.counter_collection.hist_ql.report()
        print(f"Gonna do a sim with paras - S:{S_tmp}")
        for i in range(sim.sim_param.NO_OF_RUNS):
            sim.reset()
            sim.do_simulation()
            cNh.count_all(sim)

        cNh.report_all(sim)

    pyplot.show()


def do_simulation_study(sim, print_queue_length=False, print_waiting_time=True):
    """
    This simulation study is different from the one made in assignment 1. It is mainly used to gather and visualize
    statistics for different buffer sizes S instead of finding a minimal number of spaces for a desired quality.
    For every buffer size S (which ranges from 5 to 7), statistics are printed (depending on the input parameters).
    Finally, after all runs, the results are plotted in order to visualize the differences and giving the ability
    to compare them. The simulations are run first for 100s, then for 1000s. For each simulation time, two diagrams are
    shown: one for the distribution of the mean waiting times and one for the average buffer usage
    :param sim: the simulation object to do the simulation
    :param print_queue_length: print the statistics for the queue length to the console
    :param print_waiting_time: print the statistics for the waiting time to the console
    """
    # TODO Task 2.7.1: Your code goes here
    # TODO Task 2.7.2: Your code goes here
    pass


if __name__ == '__main__':
    task_2_7_1()
    task_2_7_2()
