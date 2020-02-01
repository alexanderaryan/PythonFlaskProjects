def strcheck(lis):
    last = lis[-1]

    stri = "".join(sorted("".join(lis[:-1])))

    cou=0
    for n in last:

        if stri.count(n) >= last.count(n):
            cou+=1

    if cou==len(last):
        print ("YES")

    else:
        print ("NO")


if __name__ == '__main__':
    x = int(input())

    for n in range(x):

        y = int(input())
        lis = []
        result=[]
        for m in range(y + 1):
            lis.extend(list(map(str, input().split())))
        (strcheck(lis))
