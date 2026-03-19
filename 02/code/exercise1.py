n = input("Enter number of students: ")

column = input("Enter the column format: ").split()
marksIndex = column.index("Marks")

total = 0

for i in range(int(n)):
    studentData = input("Enter student data: ").split()
    total += int(studentData[marksIndex])

avg = total / int(n)
print(f"Average Marks: {avg:.2f}")