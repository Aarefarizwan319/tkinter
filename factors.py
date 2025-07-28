def factors(number):
    print("The factors of number are: ")
    for i in range(1, number+1):
        if number % i == 0:
            print(i)

number = int(input("Enter the number of which you want factors: "))
factors(number)
