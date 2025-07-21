with open("example.txt", "r") as file:
    contents = file.read()
    print(contents)

with open("example.txt", "w") as file:
    file.write("My name is Zodo. I enjoy coding and designing.")

with open("example.txt", "a") as file:
    file.write("\nMy favorite subject is Computer Science.")
