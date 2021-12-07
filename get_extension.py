file = "file.min.png"

files = [
    "file.min.png",
    "file.min.cpp",
    "file.css",
    "file.py",
    "file.js",
    "file.png",
]

# dotIndex = (len(file) - file.rfind(".", 1))*(-1)
# print(len(file))
# print(file.rfind(".", 1))
# print(file[:dotIndex])

# print("Mi manera")

for file in files:
    dotIndex = file.rfind(".", 1)
    print(file[dotIndex:])