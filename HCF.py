numberLargest = int(input("Enter largest number: "))
numberSmallest = int(input("Enter smallest number: "))

while numberSmallest:
    numberStore = numberSmallest
    numberSmallest = numberLargest % numberSmallest
    numberLargest = numberStore

print("HCF is: ", numberLargest)
