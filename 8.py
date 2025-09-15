num = int(input("Enter your number: "))

def is_power_of_8(n):
    if n < 1:
        return False
    while n % 8 == 0:
        n = n // 8
    return n == 1


if is_power_of_8(num):
    print(f"Yes {num} is the power of 8")
else:
    print(f"No {num} is not the power of 8")
