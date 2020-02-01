def divby():
    for num in range(2000, 3201):
        if num % 7 == 0 and num % 5 != 0:
            print(num, end=",")


if __name__== '__main__':
    divby()