
def reverse_bits(num, bit_size=32):
    binary = bin(num)[2:].zfill(bit_size)
    
   
    reversed_binary = binary[::-1]
    

    return int(reversed_binary, 2)


num = int(input("Enter a number: "))

result = reverse_bits(num)
print(f"Original number: {num}")
print(f"Reversed bit number: {result}")
