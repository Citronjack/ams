import heapq
import random


class EventChain(object):
    """
    This class contains a queue of events.

    Events can be inserted and removed from queue and are sorted by their time.
    Always the oldest event is removed.
    """

    def __init__(self):
        """
        Initialize variables and event chain
        """
        self.event_list = []

    def insert(self, event):
        """
        Inserts event e to the event chain. Event chain is sorted during insertion.
        :param: e is of type SimEvent

        """
        # TODO Task 1.2.2: Your code goes here
        heapq.heappush(self.event_list, event)


    def remove_oldest_event(self):
        """
        Remove event with smallest timestamp (if timestamps are equal then smallest priority value i.e.
        highest priority event) from queue
        :return: next event in event chain
        """
        # TODO Task 1.2.2: Your code goes here
        return heapq.heappop(self.event_list)


class SimEvent(object):
    """
    SimEvent represents an abstract type of simulation event.

    Contains mainly abstract methods that should be implemented in the subclasses.
    Comparison for EventChain insertion is implemented by comparing first the timestamps and then the priorities
    """

    def __init__(self, sim, timestamp):
        """
        Initialization routine, setting the timestamp of the event and the simulation it belongs to.
        """
        self.timestamp = timestamp
        self.priority = 0
        self.sim = sim

    def process(self):
        """
        General event processing routine. Should be implemented in subclass
        """
        raise NotImplementedError("Please Implement method \"process\" in subclass of SimEvent")

    def __lt__(self, other):
        """
        Comparison is made by comparing timestamps. If time stamps are equal, priorities are compared.
        """
        # TODO Task 1.2.1: Your code goes here
        if self.timestamp < other.timestamp:
            return True
        if self.timestamp > other.timestamp:
            return False
        if self.timestamp == other.timestamp:
            if self.priority < other.priority:
                return True
            else:
                return False


class CustomerArrival(SimEvent):
    """
    Defines a new customer arrival event (new packet comes into the system)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new customer arrival event with given execution time.

        Priority of customer arrival event is set to 1 (second highest)
        """
        super(CustomerArrival, self).__init__(sim, timestamp)
        self.priority = 1

    def process(self):
        """
        Processing procedure of a customer arrival.

        Implement according to the task description.
        """
        # TODO Task 1.3.2: Your code goes here
        iat = self.sim.sim_param.IAT
        evnet = CustomerArrival(self.sim, self.sim.sim_state.now + iat)
        self.sim.event_chain.insert(evnet)

        if self.sim.system_state.add_packet_to_server():
            self.sim.sim_state.packet_accepted()
            service_time = random.randint(1, 1000)
            event = ServiceCompletion(self.sim, self.sim.sim_state.now + service_time)
            self.sim.event_chain.insert(event)

        elif self.sim.system_state.add_packet_to_queue():
            self.sim.sim_state.packet_accepted()

        else:
            self.sim.sim_state.packet_dropped()

        "An example of bad programming bnecause when you change the system everything goes to shit!"
        # my stuff would haven worked because I would have raised out the unctions in a different way so that it can
        # be checked of a packed should be added to the queue without raising the buffer content, for example with a
        # peak flag!1

        # if not self.sim.system_state.add_packet_to_queue(True):
        #     self.sim.sim_state.packet_dropped()
        # else:  # either buffer or process
        #     if self.sim.system_state.add_packet_to_server():
        #         service_time = random.randint(1, 1000)
        #         # print(service_time)
        #         event = ServiceCompletion(self.sim, self.sim.sim_state.now + service_time)
        #         self.sim.event_chain.insert(event)
        #     else:
        #         self.sim.system_state.add_packet_to_queue()
        #     self.sim.sim_state.packet_accepted() # same for queue and processed packets


class ServiceCompletion(SimEvent):
    """
    Defines a service completion event (highest priority in EventChain)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new service completion event with given execution time.

        Priority of service completion event is set to 0 (highest).
        """
        super(ServiceCompletion, self).__init__(sim, timestamp)
        self.priority = 0

    def process(self):
        """
        Processing procedure of a service completion.

        Implement according to the task description
        """
        # TODO Task 1.3.3: Your code goes here
        self.sim.system_state.complete_service()
        # if somethiong in buffer start service again
        if self.sim.system_state.start_service():
            event = ServiceCompletion(self.sim, self.sim.sim_state.now + random.randint(1, 1000))
            self.sim.event_chain.insert(event)


class SimulationTermination(SimEvent):
    """
    Defines the end of a simulation. (least priority in EventChain)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new simulation termination event with given execution time.

        Priority of simulation termination event is set to 2 (lowest)
        """
        super(SimulationTermination, self).__init__(sim, timestamp)
        self.priority = 2

    def process(self):
        """
        Implement according to the task description.
        """
        # TODO Task 1.3.1: Your code goes here
        self.sim.sim_state.stop = True
