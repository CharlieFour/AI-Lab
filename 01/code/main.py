marks = int(input("Enter your marks: "))

if marks >= 95 and marks <= 100:
    print ("Grade: A")
elif marks >= 90 and marks < 95:
    print ("Grade: B")
elif marks >= 85 and marks < 90:
    print ("Grade: C")
elif marks >= 80 and marks < 85:
    print ("Grade: D")
else:
    print ("Grade: F")