string = input("Enter the String: ")
subString = input("Enter the Substring: ")

count = 0

for i in range(len(string) - len(subString) + 1):
    if string[i:i + len(subString)] == subString:
        count += 1
print(count)