def analyze_time_complexity(n):
    complexities = []
    
    first_loop = "O(n)"
    complexities.append(first_loop)
    print(f"First Loop: {first_loop}")
    
    second_loop = "O(log n)"
    complexities.append(second_loop)
    print(f"Second Loop: {second_loop}")
    
    third_loop = "O(1)"
    complexities.append(third_loop)
    print(f"Third Loop: {third_loop}")
    
    total_complexity = "O(n)"
    print(f"\nTotal Time Complexity: {total_complexity}")

n = int(input("Enter the value of n: "))
analyze_time_complexity(n)