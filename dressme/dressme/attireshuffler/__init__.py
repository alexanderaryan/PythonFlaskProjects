

if __name__ == '__main__':
    shirt = ['blue shirt',"yellow shirt","white tshrit"]
    pants = ['black chino','green formal','grey checked']

    combo = [(s,p) for s in shirt for p in pants]

    for n in combo:
        print (n)

