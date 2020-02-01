def fact(x):
    val = 1
    for n in range(x, 1, -1):
        val = val * n
    print(val, end=",")


if __name__=='__main__':
    fact(9)