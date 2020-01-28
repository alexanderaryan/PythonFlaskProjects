def cap():
    strin= ([x for x in input('Enter string').split(' ')])
    print (" ".join(sorted(list(set(strin)))))





if __name__ == '__main__':
    cap()