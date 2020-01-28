class Getandprint(object):
    def __init__(self):
        self.upper = ""

    def getstring(self):
        self.upper = input("print the string")

    def upperstring(self):
        print(self.upper.upper())


if __name__ == '__main__':
    c = Getandprint()
    c.getstring()
    c.upperstring()