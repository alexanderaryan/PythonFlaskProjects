def lettercount():
    letter=0
    digit=0
    x=input()
    for value in x:
        if value.isalpha():
            letter+=1
        elif value.isalnum():
            digit+=1
    print ("Letters: ",letter)
    print ("Digit: ",digit)
if __name__ == '__main__':
    lettercount()