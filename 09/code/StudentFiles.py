import re
import csv
import os

email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

def process_file(input_file):
    results = []

    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()

            for line in lines:
                data = line.strip().split(',')

                # Skip invalid lines
                if len(data) != 3:
                    continue

                name, marks, email = data

                try:
                    marks = int(marks)
                except:
                    continue

                issues = []

                # Check marks
                if marks < 12:
                    issues.append("Low Marks")

                # Validate email
                if not re.match(email_pattern, email):
                    issues.append("Invalid Email")

                # Status
                if issues:
                    status = ", ".join(issues)
                else:
                    status = "OK"

                # Store structured data
                results.append([name, marks, email, status])

        return results

    except FileNotFoundError:
        print("❌ File not found!")
        return None


# MAIN PROGRAM

print("Current Directory:", os.getcwd())

input_file = input("\nEnter input CSV file name: ")

output_data = process_file(input_file)

if output_data is not None:

    print("\n--- OUTPUT ---")
    for row in output_data:
        print(f"{row[0]} | Marks: {row[1]} | Email: {row[2]} | {row[3]}")

    # Ask user for output option
    choice = input("\nDo you want to \n(1) Append or \n(2) Create new file? \nEnter 1 or 2: ")

    if choice == '1':
        output_file = input("Enter output CSV file name to append: ")
        mode = 'a'
    else:
        output_file = input("Enter new output CSV file name: ")
        mode = 'w'

    # Ensure file ends with .csv
    if not output_file.endswith(".csv"):
        output_file += ".csv" #check the extension and add .csv if not present

    # Write to CSV
    with open(output_file, mode, newline='') as file:
        writer = csv.writer(file)

        # Write header only if new file
        if mode == 'w':
            writer.writerow(["Name", "Marks", "Email", "Status"])

        for row in output_data:
            writer.writerow(row)

    print(f"\n✅ Output successfully saved in '{output_file}'")