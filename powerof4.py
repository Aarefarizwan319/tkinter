def power4(number):
    count = 0
    if (number > 0 and (number & (number - 1)) == 0):
        while (number > 1):
            number = number >> 1
            count += 1
        if (count % 2 == 0):
            return True
        
        else:
           return False

n = int(input("Enter a number: "))
if power4(n):
    print("\nThe number is a power of 4")
else:
    print("\nThe number is not a power of 4")
