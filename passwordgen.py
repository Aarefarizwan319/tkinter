import random
import string

length = int(input("Enter the desired password length: "))

characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
password = ''.join(random.choice(characters) for _ in range(length))

print("Generated Password:", password)
