def test(n):
    iteration = 0
    for i in range(n):
        for j in range(n):
            print('.', end='-')
            iteration+=1
    print(f"\nwhen n is {n}, iteration {iteration}")
test(5)
test(4)
test(3)
print("n with every 'n' the taken = n**2")
print("n(2)")