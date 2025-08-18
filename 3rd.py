def computePower(x, y):
    result = 1
    while y>0:
        if(y%2==0):
            x=x*x
            y>>=1
        else:
            result = result * x
            y = y - 1
    return result

x = int(input("Enter x for x^y: "))
y = int(input("Enter y for x^y: "))
print("Total is", (computePower(x, y)))
