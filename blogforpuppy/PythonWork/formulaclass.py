from math import sqrt
class sqrootofnumbers(object):
    c=50

    def __init__(self,h=30):
        self.h = h

    def getstring(self):
        self.input = input("print the number in comma separated value")

    def sqwithformula(self):
        self.x=self.input.split(',')
        for n in self.x:
            y= round((2*self.c*int(n))/self.h)
            print (int(sqrt(y)),end=",")


if __name__ == '__main__':
    c = sqrootofnumbers()
    c.getstring()
    c.sqwithformula()