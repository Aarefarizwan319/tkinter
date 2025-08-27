def longest_consecutive_ones(n):
    # Convert number to binary (without '0b' prefix)
    binary_str = bin(n)[2:]
    
    # Split by '0' and find the longest sequence of '1's
    longest = max(len(seq) for seq in binary_str.split('0'))
    
    return longest

# Input from user
num = int(input("Enter your number: "))
result = longest_consecutive_ones(num)
print("Longest consecutive 1’s length :", result)
