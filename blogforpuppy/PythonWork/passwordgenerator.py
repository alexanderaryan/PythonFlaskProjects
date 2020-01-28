x='n'
y=[x for x in range(1,7)]
print (y)
li=list(map(chr,[x for x in range(97,123)]))
print (li)

for n in li:
    for m in li:
        for i in y:
            print (x+n+m+str(i))

