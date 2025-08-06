num1 = int(input("Enter Largest number : "))
num2 = int(input("Enter Smallest number : "))

if num1 > num2:
    greater = num1
else:
    greater = num2

while True:
    if greater % num1 == 0 and greater % num2 == 0:
        lcm = greater
        break
    greater += 1

print("LCM is :", lcm)
