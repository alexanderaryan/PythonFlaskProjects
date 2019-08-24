def cap():
    lst=[]
    while True:
        x=input('enter a para')
        if x:
            lst.append (x.upper())
        else:
            break
    #print (lst)
    print (" ".join(lst))



if __name__ == '__main__':
    cap()