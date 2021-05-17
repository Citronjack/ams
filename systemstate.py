__author__ = 'Alexander Prommesberger'
__matriclenumber__ = '03688679'

from finitequeue import FiniteQueue
from packet import Packet

class SystemState(object):
    
    """
    This class represents the state of our system.

    It contains information about whether the server is busy and how many customers
    are waiting in the buffer (buffer). The buffer represents the physical buffer or
    memory of our system, where packets are stored before they are served.

    The integer variable buffer_content represents the buffer fill status, the flag
    server_busy indicates whether the server is busy or idle.

    The simulation object is only used to determine the maximum buffer space as
    determined in its object sim_param.
    """

    def __init__(self, sim):
        """
        Create a system state object
        :param sim: simulation object for determination of maximum number of stored
        packets in buffer
        :return: system_state object
        :var self.served_packet:  represents current being served served_packet
        """
        self.server_busy = False
        # self.buffer_content = 0
        self.buffer = FiniteQueue(sim)
        self.sim = sim
        self.served_packet = Packet(sim)  # represents current being served served_packet
        self.last_arrival = 0

    def add_packet_to_server(self):
        """
        Try to add a served_packet to the server unit.
        :return: True if server is not busy and served_packet has been added successfully.
        """
        if not self.server_busy:
            self.served_packet = Packet(self.sim, self.sim.sim_state.now-self.last_arrival) #if self.buffer.is_empty() else self.buffer.remove()
            self.served_packet.start_service()
            self.last_arrival = self.sim.sim_state.now
            self.server_busy = True
            return True
        else:
            return False
        # if not self.server_busy:
        #     self.server_busy = True
        #     return True
        # else:
        #     return False

    def add_packet_to_queue(self, peak=False):
        """
        Try to add a served_packet to the buffer.
        :return: True if buffer/buffer is not full and served_packet has been added successfully.
        """
        packet = Packet(self.sim, self.sim.sim_state.now-self.last_arrival)
        self.last_arrival = self.sim.sim_state.now
        return self.buffer.add(packet)

        # if self.buffer_content < self.sim.sim_param.S:  # and self.server_busy error in tests
        #     self.buffer_content += 1 if peak is False else 0
        #     return True
        # else:
        #     return False

    def complete_service(self):
        """
        Reset server status to idle after a service completion.
        """
        # TODO Task 1.1.3: Your code goes here
        #self.buffer_content = 0 # correct? -- No worng!
        self.server_busy = False
        # TODO Task 2.4.3: Your code goes here somewhere
        packet = self.served_packet
        packet.complete_service()
        self.sim.counter_collection.count_packet(packet)
        self.served_packet = None  # 0 # ATT! 0 DOES NOT WORK!

    def start_service(self):
        """
        If the buffer is not empty, take the next served_packet from there and serve it.
        :return: True if buffer is not empty and a stored served_packet is being served.
        """
        if not self.buffer.is_empty():
            self.served_packet = self.buffer.remove()
            self.served_packet.start_service()
            self.server_busy = True
            return True
        else:
            return False

        # # TODO Task 1.1.3: Your code goes here
        # if self.buffer_content > 0:
        #     self.buffer_content -= 1
        #     self.server_busy = True
        #     return True
        # else:
        #     return False

    def get_queue_length(self):
        return self.buffer.get_queue_length()
