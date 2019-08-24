import random
def randomgen(low,high,num):
    for value in range(num):
        yield (random.randint(low,high))

x=randomgen(1,10,12)

print (list(x))