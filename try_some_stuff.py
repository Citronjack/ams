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



#pp.show()

a = [1,2,3,5,7,88,9,54,65]
a.sort()
b = a.index(54)
print(a)

pp.figure()
b = ['erster', 'zweriter']
for i in range(2):
    pp.plot(a, label=f"{b[i]}")
pp.legend()
pp.show()
#
# def trymebitch(me):
#     return True if me else False
#
# print(trymebitch(True))
#
# histogram1, bins1 = numpy.histogram([i % 7 for i in range(5, 50)], bins=range(0, 7))
# histogram2, bins2 = numpy.histogram([i % 7 for i in range(10, 55)], bins=range(0, 7))
#
# width_of_bins = (bins1[1] - bins1[0]) / 2
# fig, ax = pp.subplots()
# rects1 = ax.bar(numpy.ndarray(bins1) - width_of_bins / 2, histogram1, label='sda', color='r')
# rects2 = ax.bar(numpy.ndarray(bins2) + width_of_bins / 2, histogram2, label='sd', color='g')
# pp.title("Side by Side stuff")
# #ax.legend()
# ax.set_xticks(bins1)
# fig.tight_layout()
#
# pp.show()
# import matplotlib
