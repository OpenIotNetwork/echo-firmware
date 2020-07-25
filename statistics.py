import math

def mean(data):
    return sum(data) / len(data)

def stdev(data):
    xbar = mean(data)
    total = total2 = 0
    for x in data:
        total += (x - xbar) ** 2
        total2 += (x - xbar)
    total -= total2 ** 2 / len(data)
    return math.sqrt(total / (len(data) - 1))
