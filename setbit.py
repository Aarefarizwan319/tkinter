def getRightmostSetBit(n):
    position = 1
    while n > 0:
        if n & 1:
            return position
        n >>= 1
        position += 1
    return 0

num = int(input("Enter number: "))
pos = getRightmostSetBit(num)
print("Position of the first set bit:", pos)
