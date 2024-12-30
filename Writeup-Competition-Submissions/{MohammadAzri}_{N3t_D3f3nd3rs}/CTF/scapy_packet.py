with open(r"decoded_output.txt", "r") as file:
    data = file.read()

# Replace spaces and tabs with binary equivalents
binary = data.replace(" ", "0").replace("\t", "1")
print(binary)
