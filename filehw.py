import os

with open("intro.txt", "w") as file:
    file.write("My name is Aarefa. I am learning Python and web development.")

with open("intro.txt", "r") as file:
    content = file.read()
    words = content.split()
    print("Words in the file:", words)

if os.path.exists("My_File.txt"):
    print("My_File.txt exists.")
else:
    print("My_File.txt does not exist.")
    with open("My_File.txt", "w") as my_file:
        my_file.write("My name is Aarefa. I am learning Python and web development.")
    print("My_File.txt has been created.")

if os.path.exists("sample_doc.txt"):
    os.remove("sample_doc.txt")
    print("sample_doc.txt has been deleted.")
else:
    print("sample_doc.txt does not exist.")
