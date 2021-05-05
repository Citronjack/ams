import heapq
from matplotlib import pyplot as pp
import numpy

h = []

heapq.heappush(h, (1, "Being born a humansssssssssssssssssssss"))
heapq.heappush(h, (1, "God creates the universe"))
heapq.heappush(h, (5, "Satan creates the universe"))


print(heapq.heappop(h))

heapq.heappop(h)


try:

    heapq.heappop(h)
    heapq.heappop(h)

except IndexError:
    print("Heaplist is empty!")



def vgl(x,y):
    return x<y

a = 1
b = 2

print(vgl(a,b))

class Parent:
    def __init__(self, sim):
        self.sup = sim


class Child(Parent):
    def __init__(self, sim):

        super().__init__(sim)


k = Child(1)
k.sup

l1 = range(0,5)
l2 = range(0,4)
l11, = pp.plot(l1)
l22, = pp.plot(l2)
pp.legend([l11, l22], ["Peter", "Gabriel"])

pp.show()



def trymebitch(me):
    return True if me else False

print(trymebitch(True))


a = [1,2,3]
print(numpy.mean(a))