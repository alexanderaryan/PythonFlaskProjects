'''
# Sample code to perform I/O:

name = input()                  # Reading input from STDIN
print('Hi, %s.' % name)         # Writing output to STDOUT

# Warning: Printing unwanted or ill-formatted data to output will cause the test cases to fail
'''

# Write your code here
testcasecount=int(input("Enter the number of test cases"))
getinput=[]

primelist=[]
def checkprime(i):
    if i>1:
        for n in range(2,i):
            if i%n==0:
                return False
            else:
                return  True

checkprime(100)
#print (primelist)
for n in range(testcasecount):
    getinput.append(str(input("Enter the time in HH MM SS")).split(' '))
b=0
g=0
for value in getinput:
    if int(value[0])<=24 and int(value[1])<=60 and int(value[2])<=60:
        if checkprime(int(value[2])):
            if int(value[0])%value[2]==0 and int(value[1])%value[2]==0 and int(value[2])<=60:
                b+=1
            else:
                g+=1


    print(b, g)





print (getinput)