
from counter import TimeIndependentCounter
from simulation import Simulation
from matplotlib import pyplot
from counter import TimeIndependentCounter
import numpy as np
from matplotlib import pyplot as pp

"""
This file should be used to keep all necessary code that is used for the simulation section in part 5
of the programming assignment. It contains tasks 5.2.1, 5.2.2, 5.2.3 and 5.2.4.
"""


def task_5_2_1(epsilon=0.0015):
    """
    Run task 5.2.1. Make multiple runs until the blocking probability distribution reaches
    a confidence level alpha. Simulation is performed for 100s and 1000s and for alpha = 90% and 95%.
    """
    results = []
    cnt_bp_list = []
    # TODO Task 5.2.1: Your code goes here
    sim = Simulation()
    sim.sim_param.RHO = 0.9
    sim.sim_param.S = 4
    for SIM_TIME in [100*1000, 1000*1000]:
        sim.sim_param.SIM_TIME = SIM_TIME
        sim.reset()
        for alpha in [0.1, 0.05]:
            sim.reset()
            cnt_bp = TimeIndependentCounter("Block prob.")
            h = 666
            runs = 0
            while h > epsilon or np.isnan(h):
                sim.reset()
                sim.do_simulation()
                cnt_bp.count(sim.sim_result.blocking_probability)
                h = cnt_bp.report_confidence_interval(alpha=alpha, print_report=False)
                runs += 1
            cnt_bp_list.append(cnt_bp.get_mean())
            results.append(runs)
            print(f"Confidence interval for SIM_TIME: {SIM_TIME} and alpha: {alpha} is: {h} ")
    # print and return result
    print(f"Mean blocking prob. {cnt_bp_list}")
    print(
        'SIM TIME:  100s; ALPHA: 10%; NUMBER OF RUNS: ' + str(results[0]) + '; TOTAL SIMULATION TIME (SECONDS): ' + str(
            results[0] * 100))
    print(
        'SIM TIME:  100s; ALPHA:  5%; NUMBER OF RUNS: ' + str(results[1]) + '; TOTAL SIMULATION TIME (SECONDS): ' + str(
            results[1] * 100))
    print('SIM TIME: 1000s; ALPHA: 10%; NUMBER OF RUNS:  ' + str(
        results[2]) + '; TOTAL SIMULATION TIME (SECONDS): ' + str(results[2] * 1000))
    print('SIM TIME: 1000s; ALPHA:  5%; NUMBER OF RUNS:  ' + str(
        results[3]) + '; TOTAL SIMULATION TIME (SECONDS): ' + str(results[3] * 1000))
    return results


def task_5_2_2(epsilon=0.0015, guard_pkts=50):
    """
    Run simulation in batches. Start the simulation with running until a customer count of n=100 or (n=1000) and
    continue to increase the number of customers by dn=n.
    Count the blocking proabability for the batch and calculate the confidence interval width of all values, that have
    been counted until now.
    Do this until the desired confidence level is reached and print out the simulation time as well as the number of
    batches.
    """
    results = []
    # TODO Task 5.2.2: Your code goes here
    sim = Simulation()
    sim.sim_param.RHO = 0.9
    sim.sim_param.S = 4
    for BATCH_SIZE in [100, 1000]:
        sim.sim_param.BATCH_SIZE = BATCH_SIZE
        for alpha in [0.1, 0.05]:
            sim.sim_param.ALPHA = alpha
            sim.reset()
            sim.do_simulation_n_limit(BATCH_SIZE, alpha, epsilon=epsilon, guard_pkts=guard_pkts)
            results.append(sim.sim_state.now)
    # print and return results
    print('BATCH SIZE:  100; ALPHA: 10%; TOTAL SIMULATION TIME (SECONDS): ' + str(results[0] / 1000))
    print('BATCH SIZE:  100; ALPHA:  5%; TOTAL SIMULATION TIME (SECONDS): ' + str(results[1] / 1000))
    print('BATCH SIZE: 1000; ALPHA: 10%; TOTAL SIMULATION TIME (SECONDS): ' + str(results[2] / 1000))
    print('BATCH SIZE: 1000; ALPHA:  5%; TOTAL SIMULATION TIME (SECONDS): ' + str(results[3] / 1000))
    return results


def task_5_2_4(epsilon=0.0015):
    """
    Plot confidence interval as described in the task description for task 5.2.4.
    We use the function plot_confidence() for the actual plotting and run our simulation several times to get the
    samples. Due to the different configurations, we receive eight plots in two figures.
    """
    # TODO Task 5.2.4: Your code goes here
    results = []
    # TODO Task 5.2.2: Your code goes here
    sim = Simulation()
    pp.subplots(8, 1, figsize=(15,15))
    pp.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.9)
    j = 0
    for RHO in [0.5, 0.9]:
        sim.sim_param.RHO = RHO
        sim.sim_param.S = 4
        for alpha in [0.1, 0.05]:
            sim.sim_param.ALPHA = alpha
            for SIM_TIME in [100*1000, 1000*1000]:
                sim.sim_param.SIM_TIME = SIM_TIME

                # plot stuff
                y_min = []
                y_max = []
                runs = []

                for i in range(100):
                    cnt_tp = TimeIndependentCounter("tp")
                    cnt_tp_mean = TimeIndependentCounter("tp_mean")
                    for _ in range(30):
                        sim.reset()
                        sim.do_simulation()
                        cnt_tp.count(sim.sim_result.system_utilization)

                    tt_half_width = cnt_tp.report_confidence_interval(alpha)
                    cnt_tp_mean.count(cnt_tp.get_mean())
                    runs.append(i)
                    y_max.append(tt_half_width+cnt_tp.get_mean())
                    y_min.append(-tt_half_width+cnt_tp.get_mean())


                calc_mean = RHO
                act_mean = cnt_tp_mean.get_mean()
                calc_mean_in_interval = 0
                act_mean_in_interval = 0
                for i in range(len(runs)):
                    if y_min[i] < calc_mean < y_max[i]:
                        calc_mean_in_interval += 1
                    if y_min[i] < act_mean < y_max[i]:
                        act_mean_in_interval += 1
                print(f"act_mean inside interval percentage {act_mean_in_interval/len(runs)}")
                print(f"calc_mean inside interval percentage {calc_mean_in_interval / len(runs)}")
                ylabel = f"TP, {RHO, alpha, SIM_TIME//1000}"
                pp.subplot(811+j)
                plot_confidence(sim, runs, y_min, y_max, calc_mean, act_mean, ylabel)
                j += 1


    # print and return results
    # print('BATCH SIZE:  100; ALPHA: 10%; TOTAL SIMULATION TIME (SECONDS): ' + str(results[0] / 1000))
    # print('BATCH SIZE:  100; ALPHA:  5%; TOTAL SIMULATION TIME (SECONDS): ' + str(results[1] / 1000))
    # print('BATCH SIZE: 1000; ALPHA: 10%; TOTAL SIMULATION TIME (SECONDS): ' + str(results[2] / 1000))
    # print('BATCH SIZE: 1000; ALPHA:  5%; TOTAL SIMULATION TIME (SECONDS): ' + str(results[3] / 1000))
    pp.show()
    #return results


def plot_confidence(sim, runs, y_min, y_max, calc_mean, act_mean, ylabel):
    """
    Plot confidence levels in batches. Inputs are given as follows:
    :param sim: simulation, the measurement object belongs to.
    :param x: defines the batch ids (should be an array).
    :param y_min: defines the corresponding lower bound of the confidence interval.
    :param y_max: defines the corresponding upper bound of the confidence interval.
    :param calc_mean: is the mean calculated from the samples.
    :param act_mean: is the analytic mean (calculated from the simulation parameters).
    :param ylabel: is the y-label of the plot
    :return:
    """
    # TODO Task 5.2.3: Your code goes here
    """
    Note: You can change the input parameters, if you prefer to.
    """
    for run in runs:
        pp.vlines(run, y_min[run], y_max[run], label=ylabel)
        pp.ylabel("System Utilization")
        pp.xlabel("run")
    pp.hlines(calc_mean, runs[0], runs[-1], label="calc. mean", linestyles="--")
    pp.hlines(act_mean, runs[0], runs[-1], label="act. mean", colors="red")
    pp.title(f"Sys. util. for alpha:{sim.sim_param.ALPHA}, Rho:{sim.sim_param.RHO}, SimTime:{sim.sim_param.SIM_TIME}")



if __name__ == '__main__':
    task_5_2_1()
    task_5_2_2()
    task_5_2_4()
