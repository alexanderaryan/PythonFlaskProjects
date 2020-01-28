def sqredict(x):
    dict = {}
    for n in range(1, x + 1):
        dict[n] = n * n
    print(dict)


if __name__=='__main__':
    sqredict(9)