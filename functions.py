# Function 1: O(n log n)
def myfunction1(n):
    if n <= 0:
        return
    for i in range(0, n + 1):
        print("Codingal")
    myfunction1(n // 2)   # Integer division
    myfunction1(n // 3)

# Function 2: O(n)
def myfunction2(n):
    if n <= 1:
        return
    print("Codingal")
    myfunction2(n - 1)

# Example usage:
print("Output of myfunction1:")
myfunction1(5)

print("\nOutput of myfunction2:")
myfunction2(5)
