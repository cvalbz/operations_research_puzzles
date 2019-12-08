from z3 import *

"""
[1, 0, 0, 0, 1, 1, 1] [5]   [12]
[1, 1, 0, 0, 0, 1, 1] [0]   [ 5]
[1, 1, 1, 0, 0, 0, 1] [0]   [ 5]
[1, 1, 1, 1, 0, 0, 0] [5] = [10]
[0, 1, 1, 1, 1, 0, 0] [7]   [12]
[0, 0, 1, 1, 1, 1, 0] [0]   [12]
[0, 0, 0, 1, 1, 1, 1] [0]   [12]
"""

# workers distribution per weekday
W = [ Int("w_%i" % i) for i in range(7) ]
cost = Int("c")

days_matrix = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1],
]
target = [4, 5, 5, 10, 12, 12, 2]

s = Optimize()
for worker in W:
    s.add( (And(0 <= worker, worker <= 6)) )

for ix, line in enumerate(range(7)):
    s.add(Sum([i * j for i, j in zip(days_matrix[ix], W)]) >= target[ix])

s.add(Sum(W) == cost)
s.minimize(cost)

s.check()
m = s.model()

print("Optimized to %s workers, saved $%s", (m[cost], 17 * 400 - m[cost] * 400))
print("Allocation per days (Monday to Sunday): %s" % str([m[w] for w in W]))

