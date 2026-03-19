input_str = input("Enter the String: ")

charCount = {}
count = 0

for i in input_str:
    if i in charCount:
        charCount[i] += 1
    else:
        charCount[i] = 1

for key, value in charCount.items():
    print(f"{key} : {value}")
