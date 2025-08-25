def printPowerSet(set, set_size):
    power_set_size = 2**set_size
    outer = 0
    inner = 0

    for outer in range(0, power_set_size):
        for inner in range(0, set_size):
            if(outer & (1 << inner)):
                print(set[inner], end = "")
        print("")

size = int(input("Enter size of set: "))
set = []
for i in range(0, size):
    set.append(input("Enter element: "))

printPowerSet(set, size)
