__author__ = 'Alexander Prommesberger'
__matriclenumber__ = '03688679'
from rng import *
from matplotlib import pyplot as pp
import numpy as np
from simulation import Simulation
"""
This file should be used to keep all necessary code that is used for the verification section in part 3 of the
programming assignment. It contains tasks 3.2.1 and 3.2.2.
"""


def task_3_2_1(bins=None, la=None):
    """
    This function plots two histograms for verification of the random distributions.
    One histogram is plotted for a uniform distribution, the other one for an exponential distribution.
    """
    # TODO Task 3.2.1: Your code goes here
    la = 5 if la is None else la
    e = ExponentialRNS(la)
    a = 0
    b = 8
    u = UniformRNS([a,b], 1)
    tot_ = 10000
    bins = bins if bins is not None else int(np.sqrt(tot_))

    e_list = [e.next() for _ in range(tot_)]
    u_list = [u.next() for _ in range(tot_)]

    pp.subplots_adjust(hspace=0.5)
    pp.subplot(2,1,1)
    pp.title("Histogram of UNIFORM distribution")
    pp.xlabel('x')
    pp.ylabel("Empirical rate of occurence")
    pp.hist(u_list, bins=bins, weights=float(1/tot_)*np.ones(tot_))

    pp.subplot(2,1,2)
    pp.title(f"Histogram of EXPONENTIAL distribution for lambda={la} with #bins={bins}")
    pp.xlabel('x')
    pp.ylabel("Empirical rate of ocurence")
    pp.hist(e_list, bins=bins, weights=float(1/tot_)*np.ones(tot_))
    print(f"Real Mean: {1/la}, empirical mean {np.mean(e_list)}, difference={np.abs(np.mean(e_list)-1/la)}")
    pp.show()


def task_3_2_2():
    """
    Here, we execute task 3.2.2 and print the results to the console.
    The first result string keeps the results for 100s, the second one for 1000s simulation time.
    """
    # TODO Task 3.2.2: Your code goes here
    pp.figure()
    sim = Simulation()
    # rhos = [0.01, 0.5, 0.8, 0.9]
    rhos = [.01, .5, .8, .9]

    for SIM_TIME in [100, 1000]:
        system_utilization_list = []
        sim.sim_param.S = 5
        # cNh = TaskCounterClass(sim, plot_per_packet)
        sim.sim_param.NO_OF_RUNS = 1000

        sim.sim_param.SIM_TIME = SIM_TIME * 1000

        for rho in rhos:
            sim.sim_param.RHO = rho
            system_utilization_mean = 0
            for i in range(sim.sim_param.NO_OF_RUNS):
                sim.reset()
                system_utilization_mean += sim.do_simulation().system_utilization
            system_utilization_list.append(system_utilization_mean/sim.sim_param.NO_OF_RUNS)

        print(f"For SIM_TIME={SIM_TIME} the mean utilization was {system_utilization_list}")

        pp.plot(rhos, system_utilization_list, label=f"SIM_TIME={SIM_TIME}", marker="*", linestyle='--')
    pp.legend()
    pp.title("System utilization in regards to the choice of rho ")
    pp.xlabel("Rho")
    pp.ylabel("System Utilization")
    pp.show()


def task_3_2_2_2():
    """
    Here, we execute task 3.2.2 and print the results to the console.
    The first result string keeps the results for 100s, the second one for 1000s simulation time.
    """
    # TODO Task 3.2.2: Your code goes here
    pp.figure()
    sim = Simulation()
    # rhos = [0.01, 0.5, 0.8, 0.9]
    rhos = [.01, .5, .8, .9]
    for S in [10, 100]:
        sim.sim_param.S = S
        for SIM_TIME in [100]:
            system_utilization_list = []
            # cNh = TaskCounterClass(sim, plot_per_packet)
            sim.sim_param.NO_OF_RUNS = 1000

            sim.sim_param.SIM_TIME = SIM_TIME * 1000

            for rho in rhos:
                sim.sim_param.RHO = rho
                system_utilization_mean = 0
                for i in range(sim.sim_param.NO_OF_RUNS):
                    sim.reset()
                    print(sim.sim_param.S)
                    system_utilization_mean += sim.do_simulation().system_utilization
                system_utilization_list.append(system_utilization_mean/sim.sim_param.NO_OF_RUNS)

            print(f"For SIM_TIME={SIM_TIME} the mean utilization was {system_utilization_list}")

            pp.plot(rhos, system_utilization_list, label=f"SIM_TIME={SIM_TIME}, S={S}", marker="*", linestyle='--')
    pp.legend()
    pp.title("System utilization in regards to the choice of rho ")
    pp.xlabel("Rho")
    pp.ylabel("System Utilization")
    pp.show()


if __name__ == '__main__':
    task_3_2_1()
    task_3_2_2()
