import numpy as np


def trim_emp_n(emp_x, emp_n, t=5):
    n_add = 0
    idx_max = np.unravel_index(emp_n.argmax(), emp_n.shape)[0]
    idxs = [i for i in range(idx_max)] + [i for i in range(len(emp_n)-1, idx_max, -1)]
    n_idxs_del = []
    x_idxs_del = []
    for i in idxs:
        if emp_n[i] < 5:
            e = 1 if i < idx_max else -1
            emp_n[i + e] += emp_n[i]
            n_idxs_del.append(i)
            x_idxs_del.append(i+e)

    emp_n = np.delete(emp_n, n_idxs_del)
    emp_x = np.delete(emp_x, x_idxs_del)
    return emp_x, emp_n


alpha = .1
values = []
values2 = []
np.random.seed(1)
for _ in range(100):
    values.append(np.random.normal(5, 1))
    values2.append(np.random.uniform(0, 10))

emp_n, emp_x = np.histogram(values, bins=20, range=(0, 10))
a,b = trim_emp_n(emp_x, emp_n)

print("fin")
