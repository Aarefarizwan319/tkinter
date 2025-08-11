for num in range(10, 100):
    for i in range(2, num):
        if num % i == 0:
            break
    else:
        print(num, end=" ")
