__author__ = 'Alexander Prommesberger'
__matriclenumber__ = '03688679'
from simstate import SimState
from systemstate import SystemState
from event import EventChain, CustomerArrival, SimulationTermination
from simresult import SimResult
from simparam import SimParam
from counter import TimeIndependentCounter
import numpy as np

from countercollection import CounterCollection
from rng import RNG, ExponentialRNS, UniformRNS


class Simulation(object):

    def __init__(self, sim_param=SimParam(), no_seed=False):
        """
        Initialize the Simulation object.
        :param sim_param: is an optional SimParam object for parameter pre-configuration
        :param no_seed: is an optional parameter. If it is set to True, the RNG should be initialized without a
        a specific seed.
        """
        self.sim_param = sim_param
        self.sim_state = SimState()
        self.system_state = SystemState(self)
        self.event_chain = EventChain()
        self.sim_result = SimResult(self)
        # TODO Task 2.4.3: Uncomment the line below
        self.counter_collection = CounterCollection(self)
        # TODO Task 3.1.2: Uncomment the line below and replace the "None"

        if no_seed:
            e1_mean = 1
            e1 = ExponentialRNS(float(1/e1_mean))
            e2_mean = (self.sim_param.RHO)
            e2 = ExponentialRNS(float(1 / e2_mean))
            #u = UniformRNS([0, sim_param.RHO], self.sim_param.SEED)
            self.rng = RNG(e1, e2)
        else:
            e1_mean = 1
            e1 = ExponentialRNS(float(1/e1_mean), self.sim_param.SEED_IAT)
            e2_mean = (self.sim_param.RHO)
            e2 = ExponentialRNS(float(1 / e2_mean), self.sim_param.SEED_ST)
            #u = UniformRNS([0, sim_param.RHO], self.sim_param.SEED)
            self.rng = RNG(e1, e2)

    def reset(self, no_seed=False):
        """
        Reset the Simulation object.
        :param no_seed: is an optional parameter. If it is set to True, the RNG should be reset without a
        a specific seed.
        """
        self.sim_state = SimState()
        self.system_state = SystemState(self)
        self.event_chain = EventChain()
        self.sim_result = SimResult(self)
        # TODO Task 2.4.3: Uncomment the line below
        self.counter_collection = CounterCollection(self)
        #self.counter_collection.reset()
        # TODO Task 3.1.2: Uncomment the line below and replace the "None"
        self.rng.iat_rns.set_parameters(1.)
        self.rng.st_rns.set_parameters(1./float(self.sim_param.RHO))
        # if no_seed:
        #     e1_mean = 1
        #     e1 = ExponentialRNS(float(1./e1_mean))
        #     e2_mean = self.sim_param.RHO
        #     e2 = ExponentialRNS(float(1. / e2_mean))
        #     #u = UniformRNS([0, sim_param.RHO], self.sim_param.SEED)
        #     self.rng = RNG(e1, e2)
        # else:
        #     e1_mean = 1
        #     e1 = ExponentialRNS(float(1./e1_mean), self.sim_param.SEED_IAT)
        #     e2_mean = self.sim_param.RHO
        #     e2 = ExponentialRNS(float(1. / e2_mean), self.sim_param.SEED_ST)
        #     #u = UniformRNS([0, sim_param.RHO], self.sim_param.SEED)
        #     self.rng = RNG(e1, e2)

    def do_simulation_sol(self):
        """
        Do one simulation run. Initialize simulation and create first and last event.
        After that, one after another event is processed.
        :return: SimResult object
        """
        # insert first and last event
        self.event_chain.insert(CustomerArrival(self, 0))
        self.event_chain.insert(SimulationTermination(self, self.sim_param.SIM_TIME))

        # start simulation (run)
        while not self.sim_state.stop:

            # get next simevent from events
            e = self.event_chain.remove_oldest_event()
            if e:
                # if event exists and timestamps are ok, process the event
                if self.sim_state.now <= e.timestamp:
                    self.sim_state.now = e.timestamp
                    self.counter_collection.count_queue()
                    e.process()
                else:
                    print('NOW: ' + str(self.sim_state.now) + ', EVENT TIMESTAMP: ' + str(e.timestamp))
                    raise RuntimeError("ERROR: TIMESTAMP OF EVENT IS SMALLER THAN CURRENT TIME.")

            else:
                print('Event chain is empty. Abort')
                self.sim_state.stop = True

        # gather results for sim_result object
        self.sim_result.gather_results()
        return self.sim_result

    def do_simulation(self):
        """
        Do one simulation run. Initialize simulation and create first and last event.
        After that, one after another event is processed.
        :return: SimResult object
        """
        # insert first and last event
        self.event_chain.insert(CustomerArrival(self, 0))
        self.event_chain.insert(SimulationTermination(self, self.sim_param.SIM_TIME))

        # start simulation (run)
        while not self.sim_state.stop:
            # TODO Task 1.4.1: Your code goes here
            # Had multiple times an empty event chain?!
            try:
                event = self.event_chain.remove_oldest_event()
            except IndexError:
                print("------------------------ Heaplist is empty! Aborting Simulation... ------------------------")
                self.sim_state.stop = True
                break

            if self.sim_state.now <= event.timestamp:
                self.sim_state.now = event.timestamp
                self.counter_collection.count_queue()
                event.process()
                # TODO Task 2.4.3: Your code goes here somewhere
            # WTF to bad to program, my timestamp were bigger than event time! - fixed, mistake in random time gern
            else:
                print(f"The Simulation time is bigger than the event time! sim_state.now={self.sim_state.now} and "
                      f"event.time={event.timestamp}")
                self.sim_state.stop = True
            """
            Hint:
            e = self.event_chain.remove_oldest_event()
            e.process()
            You can use and adapt the following lines in your realization
            """

        # gather results for sim_result object
        self.sim_result.gather_results()
        return self.sim_result

    def do_simulation_n_limit(self, BATCH_SIZE, alpha, epsilon=0.0015, guard_pkts=50):
        """
        Call this function, if the simulation should stop after a given number of packets
        Do one simulation run. Initialize simulation and create first event.
        After that, one after another event is processed.
        :param n: number of customers, that are processed before the simulation stops
        :return: SimResult object
        """
        # insert first event
        self.event_chain.insert(CustomerArrival(self, 0))
        # block prob couter
        cnt_pb = TimeIndependentCounter("bp")
        guard_active = False
        assert guard_pkts < BATCH_SIZE, "guard_pkts should be smaller than the BATCH_SIZE!"
        # start simulation (run)
        while not self.sim_state.stop:
            # TODO Task 4.3.2: Your code goes here
            # TODO Task 5.2.2: Your code goes here
            try:
                event = self.event_chain.remove_oldest_event()
            except IndexError:
                print("------------------------ Heaplist is empty! Aborting Simulation... ------------------------")
                self.sim_state.stop = True
                break

            if self.sim_state.now <= event.timestamp:
                self.sim_state.now = event.timestamp
                self.counter_collection.count_queue()
                event.process()
                if event.priority == 0:
                    self.counter_collection.served_pkts += 1
                if self.counter_collection.served_pkts == guard_pkts and guard_active:
                    guard_active = False
                    self.counter_collection.served_pkts = 0
                if self.counter_collection.served_pkts == BATCH_SIZE:
                    self.counter_collection.served_pkts = 0
                    guard_active = True
                    bp = self.sim_state.get_blocking_probability()
                    cnt_pb.count(bp)
                    if cnt_pb.report_confidence_interval(alpha, False) < epsilon and not np.isnan(cnt_pb.report_confidence_interval(alpha, False)):
                        print(f"Conf. intervall for BATCHES:{self.sim_param.BATCH_SIZE} and alpha: {self.sim_param.ALPHA}"
                              f" is {(cnt_pb.report_confidence_interval(alpha, False))}")
                        self.sim_state.stop = True
                    self.sim_state.reset() if self.sim_state.stop is False else -1
            else:
                self.sim_state.stop = True
                raise RuntimeError(f"The Simulation time is bigger than the event time! sim_state.now={self.sim_state.now} and "
                      f"event.time={event.timestamp}")
            # if self.counter_collection.served_pkts == n: # This implementation lead to error --> packets not counted correctly, packet is served if prority==0
        self.sim_result.gather_results()
        return self.sim_result

        # gather results for sim_result object
        #raise RuntimeError(f"do_simulation_n_limit has ended before the limit was reached! \n rho={self.sim_param.RHO}")
