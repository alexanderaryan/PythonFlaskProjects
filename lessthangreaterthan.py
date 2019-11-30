def checkfunc(val,maxR):
    resul=[]
    for n in range(len(val)):
        print (val[n], maxR[n])
        x = "".join(val[n])
        if x.count('<')!=x.count('>'):
            y=x.replace('>','<>',maxR[n])
            if y.count('<')==y.count('>'):
                resul.append(1)
                print (y,'is')
            else:
                resul.append(0)
                print (y,"not")
        else:
            resul.append(1)
            print (x,'aa')


    print(resul)





if __name__ =='__main__':
    x=int(input())
    val=[]
    maxR=[]
    for n in range(x):
        val.extend(list(map(str, input().split())))

    max=int(input())
    for m in range(max):
        maxR.extend(list(map(int, input().split())))

    checkfunc (val,maxR)