# Function using 1 iteration (direct multiplication)
def multiply_once(a, b):
    return a * b

# Function using N iterations (repeated addition)
def multiply_n_times(a, b):
    result = 0
    for _ in range(b):  # repeat 'a' added to result 'b' times
        result += a
    return result

# Taking inputs
a = int(input("Enter 'a' for a*b : "))
b = int(input("Enter 'b' for a*b : "))

# Output
print("\n1 iteration: ", multiply_once(a, b))
print("N iteration: ", multiply_n_times(a, b))
