def squaregen(n):
    for number in range(n):
        yield (number*number)

x=squaregen(10)

print (list(x))