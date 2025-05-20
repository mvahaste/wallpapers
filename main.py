import os

x = os.walk(".")

print("Current Directory:", os.getcwd())

print("List of direct subdirectories:")

for root, dirs, files in x:
    for dir in dirs:
        print(dir)

    break
