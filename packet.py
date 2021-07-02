


class Packet(object):

    """
    Packet represents a data packet processed by the DES.

    It contains variables for measurements, which include timestamps (arrival, service start, service completion)
    and the status of the packet (served, completed).
    """

    def __init__(self, sim, iat=None):
        """
        Initialize a packet with its arrival time and (optionally) the inter-arrival time w.r.t. the last packet.
        :param sim: simulation, the packet belongs to
        :param iat: inter-arrival time with respect to the last arrival
        :return: packet object
        """
        self.sim = sim

        self.t_arrival = sim.sim_state.now
        self.t_start = -1
        self.t_complete = -1
        self.iat = iat

        self.waiting = True
        self.served = False
        self.completed = False

    def start_service(self):
        """
        Change the status of the packet once the serving process starts.
        """
        # TODO Task 2.1.1: Your code goes here
        self.waiting = False
        self.served = True
        self.t_start = self.sim.sim_state.now
        
    def complete_service(self):
        """
        Change the status of the packet once the serving process is completed.
        """
        # TODO Task 2.1.1: Your code goes here
        self.completed = True
        self.served = False  # unsure about this one
        self.t_complete = self.sim.sim_state.now

    def get_waiting_time(self):
        """
        Return the waiting time of the packet. An error occurs when the packet has not been served yet.
        :return: waiting time
        """
        # TODO Task 2.1.1: Your code goes here
        if not self.served and not self.completed:
            raise Exception("Oh no, a terrible thing has happened! Worse than SATAN! An error in your code. "
                            "get_waiting_time was called when the packed was not waiting yet!")

        return self.t_start - self.t_arrival
    
    def get_service_time(self):
        """
        Calculate and return the service time
        :return: service time
        """
        # TODO Task 2.1.1: Your code goes here
        return self.t_complete - self.t_start

    def get_system_time(self):
        """
        Calculate and return the system time (waiting time + service time)
        :return: system time (waiting time + serving time)
        """
        # TODO Task 2.1.1: Your code goes here
        return self.t_complete - self.t_arrival

    def get_interarrival_time(self):
        """
        Return the inter-arrival time between the current and the last customer/packet
        :return: inter-arrival time
        """
        # TODO Task 2.1.1: Your code goes here
        return self.iat
