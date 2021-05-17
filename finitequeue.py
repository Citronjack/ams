__author__ = 'Alexander Prommesberger'
__matriclenumber__ = '03688679'
import queue


class FiniteQueue(object):
    """
    Class representing a finite queue representing the system buffer storing packets.

    It is a FIFO queue with finite capacity. Methods contain adding and removing packets
    as well as checking the fill status of the FIFO. Clearing the queue is done with the method flush.
    """

    def __init__(self, sim):
        """
        Initialize the finite queue
        :param sim: simulation object, that the queue belongs to
        :return: FiniteQueue object
        """
        self.sim = sim
        self.buffer = queue.Queue()

    def add(self, packet):
        """
        Try to add a packet to the queue
        :param packet: packet which is supposed to be queued
        :return: true if packet has been enqueued, false if rejected
        """
        # TODO Task 2.2.1: Your code goes here
        if self.get_queue_length() < self.sim.sim_param.S:
            self.buffer.put(packet)
            return True
        else:
            return False

    def remove(self):
        """
        Return the first packet in line and remove it from the FIFO
        :return: first packet in line
        """
        # TODO Task 2.2.1: Your code goes here
        return self.buffer.get()  # Mark for latter, could be problematic if called when queue empty!

    def get_queue_length(self):
        """
        :return: fill status of the queue (queue length)
        """
        # TODO Task 2.2.1: Your code goes here
        return self.buffer.qsize()

    def is_empty(self):
        """
        :return: true if queue is empty
        """
        # TODO Task 2.2.1: Your code goes here
        return self.buffer.empty()
        #  return True if self.get_queue_length() == 0 else False

    def flush(self):
        """
        erase/delete all packets from the FIFO
        """
        # TODO Task 2.2.1: Your code goes here
        while not self.is_empty():
            self.buffer.get()
