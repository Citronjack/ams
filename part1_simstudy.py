from simparam import SimParam
from simulation import Simulation
import random
from matplotlib import pyplot as pp

"""
This file should be used to keep all necessary code that is used for the simulation study in part 1 of the programming
assignment. It contains the tasks 1.7.1, 1.7.2 and 1.7.3.

The function do_simulation_study() should be used to run the simulation routine, that is described in the assignment.
"""


def task_1_7_1(run_time=100000):
    """
    Execute task 1.7.1 and perform a simulation study according to the task assignment.
    :return: Minimum number of buffer spaces to meet requirements.
    """
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim_param.SIM_TIME = run_time
    sim = Simulation(sim_param)
    return do_simulation_study(sim)


def task_1_7_2(run_time=1000000):
    """
    Execute task 1.7.2 and perform a simulation study according to the task assignment.
    :return: Minimum number of buffer spaces to meet requirements.
    """
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim_param.SIM_TIME = run_time
    sim_param.MAX_DROPPED = 100
    sim_param.NO_OF_RUNS = 100
    sim = Simulation(sim_param)
    return do_simulation_study(sim)


def task_1_7_3():
    """
    Execute task 1.7.3.
    """
    # TODO Task 1.7.3: Your code goes here (if necessary)
    ###### Sim 1

    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim_param.SIM_TIME = 100*1000
    sim_param.MAX_DROPPED = 10
    sim_param.NO_OF_RUNS = 1000
    sim = Simulation(sim_param)
    S, percentage_packet_drop_list_1 = do_simulation_study_adj(sim)
    print("Finished with SIm 1")
    ###### Sim 2

    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim_param.SIM_TIME = 1000 * 1000
    sim_param.MAX_DROPPED = 100
    sim_param.NO_OF_RUNS = 1000
    sim = Simulation(sim_param)
    S, percentage_packet_drop_list_2 = do_simulation_study_adj(sim)
    print("Finished with SIm 2")
    ###### Sim 3

    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim_param.SIM_TIME = 10000 * 1000
    sim_param.MAX_DROPPED = 1000
    sim_param.NO_OF_RUNS = 1000
    sim = Simulation(sim_param)
    S, percentage_packet_drop_list_3 = do_simulation_study_adj(sim)
    print("Finished with SIm 3")

    l1, = pp.plot(range(1, len(percentage_packet_drop_list_1)+1), percentage_packet_drop_list_1)
    l2, = pp.plot(range(1, len(percentage_packet_drop_list_2) + 1), percentage_packet_drop_list_2)
    l3, = pp.plot(range(1, len(percentage_packet_drop_list_3) + 1), percentage_packet_drop_list_3)
    pp.xlabel("Queue Size")
    pp.ylabel("Percentage of blocked packets")
    pp.title("Comparison of Simulation result for different Simulation parameters")
    pp.legend([l1, l2, l3], ['100', '1000', '10000'])
    pp.show()
    print("Finished...")
    return True


def do_simulation_study_adj(sim, S_starting_point=0):
    sim.sim_param.S = S_starting_point
    percentage_packet_drop_list = []
    while True:
        sim.reset()
        sim.sim_param.S += 1
        lt_10_pkts_dropped_counter = 0
        for _ in range(sim.sim_param.NO_OF_RUNS):
            sim.do_simulation()
            sim_results = sim.sim_result.packets_dropped
            sim.reset()
            if sim_results < sim.sim_param.MAX_DROPPED:
                lt_10_pkts_dropped_counter += 1
        percentage_packet_drop_list.append(lt_10_pkts_dropped_counter / sim.sim_param.NO_OF_RUNS)
        if lt_10_pkts_dropped_counter / sim.sim_param.NO_OF_RUNS >= 0.95:
            return sim.sim_param.S, percentage_packet_drop_list


def do_simulation_study(sim, S_starting_point=0):
    """
    Implement according to task description.
    """
    # TODO Task 1.7.1: Your code goes here
    sim.sim_param.S = S_starting_point
    while True:
        sim.reset()
        sim.sim_param.S += 1
        lt_10_pkts_dropped_counter = 0
        for i in range(sim.sim_param.NO_OF_RUNS):
            sim.do_simulation()
            sim_results = sim.sim_result.packets_dropped
            # print(sim_results)
            # time.sleep(0.2)
            sim.reset()
            if sim_results < sim.sim_param.MAX_DROPPED:
                lt_10_pkts_dropped_counter += 1
        if lt_10_pkts_dropped_counter/sim.sim_param.NO_OF_RUNS >= 0.8:
            print(
                f"Buffer Size: {sim.sim_param.S}: Less than 10 packets dropped percentage: {lt_10_pkts_dropped_counter / sim.sim_param.NO_OF_RUNS}")
            print(f"Minimal buffer Size: {sim.sim_param.S}")
            return sim.sim_param.S
        else:
            print(
                f"Buffer Size: {sim.sim_param.S}: Less than 10 packets dropped percentage: {lt_10_pkts_dropped_counter / sim.sim_param.NO_OF_RUNS}")


if __name__ == '__main__':
    task_1_7_1()
    task_1_7_2()
    task_1_7_3()
