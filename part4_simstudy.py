__author__ = 'Alexander Prommesberger'
__matriclenumber__ = '03688679'
"""
This file should be used to keep all necessary code that is used for the verification and simulation section in part 4
of the programming assignment. It contains tasks 4.2.1, 4.3.1 and 4.3.2.
"""
import simulation
from counter import *
from rng import *
from matplotlib import pyplot as pp
import numpy as np
from simulation import Simulation


def task_4_2_1(k = 1000, do_compare=False):
    """
    Execute exercise 4.2.1, which is basically just a test for the auto correlation.
    """
    # TODO Task 4.2.1: Your code goes here
    ticcc = TimeIndependentCrosscorrelationCounter("Cross Corr.")
    "max_lag=1 or 2 since the sequence has period 2 or 3"
    ticac_s1 = TimeIndependentAutocorrelationCounter("Auto Corr. for s1", max_lag=1)
    ticac_s2 = TimeIndependentAutocorrelationCounter("Auto Corr. for s2", max_lag=2)
    print(f"k={k} -------------------------------------------------------------------")
    seq1 = [1, -1]*3*k
    seq2 = [1, 1, -1]*2*k
    for s1, s2 in zip(seq1, seq2):
        ticac_s1.count(s1)
        ticac_s2.count(s2)
        ticcc.count(s1, s2)
    "Values explained in jupyter notebook"
    #print(f"Seq1 mean: {numpy.array(seq1).mean()} var: {numpy.array(seq1).var(ddof=1)}")
    #print(f"Seq2 mean: {numpy.array(seq2).mean()} var: {numpy.array(seq2).var(ddof=1)}")
    ticcc.report()
    ticac_s1.report()
    ticac_s2.report()
    if do_compare:
        lecture_formula_cov_corr(seq1, max_lag=1, k=k, name="Seq.1")
        lecture_formula_cov_corr(seq2, max_lag=2, k=k, name="Seq.2")


def lecture_formula_cov_corr(seq, max_lag, k=1000, name="Default"):
    print(f" ---- Cov. & Corr. for {name} with different formular for k={k} ----")
    for lag in range(max_lag+1):
        arr_1 = numpy.array(seq) - numpy.array(seq).mean()
        arr_2 = numpy.array(seq[-1 * lag:] + seq[:-1 * lag]) - numpy.array(seq[-1 * lag:] + seq[:-1 * lag]).mean()
        cov = arr_1.dot(arr_2) / (arr_1.size - 1)
        corr = cov/numpy.var(seq, ddof=1)
        print(f"Cov: {cov}, Corr. {corr}")


def task_4_3_1():
    """
    Run the correlation tests for given rho for all correlation counters in counter collection.
    After each simulation, print report results.
    SIM_TIME is set higher in order to avoid a large influence of startup effects
    """
    # TODO Task 4.3.1: Your code goes here
    pp.figure()
    sim = Simulation()

    sim.sim_param.S = 10000
    sim.sim_param.SIM_TIME = 10000*10**3
    rhos = [.01, .5, .8, .9]
    for rho in rhos:
        print(f"rho={rho} ------------------------------------------")
        sim.sim_param.RHO = rho
        sim.reset()
        #for _ in range(sim.sim_param.NO_OF_RUNS):
        sim.do_simulation()
        sim.counter_collection.report()
        pp.plot(range(sim.counter_collection.acnt_wt.max_lag+1), sim.counter_collection.acnt_wt.report_return(), label=f"rho={rho}", marker='*')
    pp.legend()
    pp.show()


def task_4_3_2():
    """
    Exercise to plot the scatter plot of (a) IAT and serving time, (b) serving time and system time
    The scatter plot helps to better understand the meaning of bit/small covariance/correlation.
    For every rho, two scatter plots are needed.
    The simulation parameters are the same as in task_4_3_1()
    """
    # TODO Task 4.3.2: Your code goes here
    sim = Simulation()

    sim.sim_param.S = 10000
    sim.sim_param.SIM_TIME = 10000 * 10 ** 3
    rhos = [.01, .5, .8, .95]

    pp.subplots(2, 4, figsize=(15,15))
    pp.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.9)
    i = 1
    for rho in rhos:
        sim.sim_param.RHO = rho
        sim.reset()
        #for _ in range(sim.sim_param.NO_OF_RUNS):
        sim.do_simulation()
        pp.subplot(240 + i)
        pp.xlabel("IAT")
        pp.ylabel("Service time (St)")
        pp.title(f"Iat vs St, rho={rho}")
        pp.scatter(sim.counter_collection.cnt_iat_st.tic_1.values, sim.counter_collection.cnt_iat_st.tic_2.values, marker='*', s=5)
        pp.subplot(244 + i)
        pp.xlabel("System Time")
        pp.ylabel("Service time (St)")
        pp.title(f"St vs SysP, rho={rho}")
        pp.scatter(sim.counter_collection.cnt_st_syst.tic_1.values, sim.counter_collection.cnt_st_syst.tic_2.values, marker='*', s=5)
        i += 1
        #sim.counter_collection.report()
    pp.show()


def task_4_3_3(seed=0):
    """
    Exercise to plot auto correlation depending on lags. Run simulation until 10000 (or 100) packets are served.
    For the different rho values, simulation is run and the waiting time is auto correlated.
    Results are plotted for each N value in a different diagram.
    Note, that for some seeds with rho=0.01 and N=100, the variance of the auto covariance is 0 and returns an error.
    """
    # TODO Task 4.3.3: Your code goes here
    sim = Simulation()

    pp.subplots(2, 1)
    pp.title(f"Auto corr., lag vs waiting time")

    sim.sim_param.S = 10*8
    sim.sim_param.SIM_TIME = 10000*10**6
    sim.sim_param.SEED = seed
    sim.sim_param.SEED_ST = seed
    sim.sim_param.SEED_IAT = seed
    rhos = [.01, .5, .8, .95]
    i = 1
    for n in [100, 10000]:
        pp.subplot(210+i)

        for rho in rhos:
            sim.sim_param.RHO = rho
            sim.reset()
            #for _ in range(sim.sim_param.NO_OF_RUNS):
            sim.do_simulation_n_limit(n)
            #sim.counter_collection.report()
            pp.plot(range(0, 21), sim.counter_collection.acnt_wt.report_return(), marker='*', label=f"rho={rho}, n={n}")
            pp.xlabel("lag")
            pp.ylabel("auto corr.")
            pp.legend()
        i += 1
    pp.show()

if __name__ == '__main__':
    task_4_2_1()
    task_4_3_1()
    task_4_3_2()
    task_4_3_3()
