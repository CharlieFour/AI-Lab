import tkinter as tk
from tkinter import ttk, messagebox
import re

class EmployeeRegistrationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Registration System")
        self.root.geometry("650x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f4f8")

        # Configure styles
        self.setup_styles()

        # Create main container with scrollbar for smaller screens
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # ==================== Header ====================
        title = ttk.Label(
            main_frame,
            text="👔 Employee Registration & Salary Utility",
            font=("Segoe UI", 16, "bold"),
            foreground="#1e3c72"
        )
        title.grid(row=0, column=0, pady=(0, 20), sticky="w")

        # ==================== Employee Info Frame ====================
        emp_frame = ttk.LabelFrame(main_frame, text="Employee Information", padding="15")
        emp_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        emp_frame.columnconfigure(1, weight=1)

        # Form fields
        fields = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Email", "email"),
            ("Department", "department")
        ]

        self.entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(emp_frame, text=label, font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", pady=5, padx=(0, 10))
            entry = ttk.Entry(emp_frame, width=30, font=("Segoe UI", 10))
            entry.grid(row=i, column=1, sticky="ew", pady=5)
            self.entries[key] = entry

        # ==================== Salary Calculation Frame ====================
        salary_frame = ttk.LabelFrame(main_frame, text="Salary Calculation", padding="15")
        salary_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        salary_frame.columnconfigure(1, weight=1)

        ttk.Label(salary_frame, text="Daily Wage ($)", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=5, padx=(0, 10))
        self.daily_wage_entry = ttk.Entry(salary_frame, width=20, font=("Segoe UI", 10))
        self.daily_wage_entry.grid(row=0, column=1, sticky="w", pady=5)

        ttk.Label(salary_frame, text="Working Days", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=5, padx=(0, 10))
        self.working_days_entry = ttk.Entry(salary_frame, width=20, font=("Segoe UI", 10))
        self.working_days_entry.grid(row=1, column=1, sticky="w", pady=5)

        # Result display
        self.salary_result = ttk.Label(salary_frame, text="Total Salary: $0.00", font=("Segoe UI", 11, "bold"), foreground="#2e7d32")
        self.salary_result.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # ==================== Buttons ====================
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=10, sticky="ew")
        button_frame.columnconfigure((0,1,2,3), weight=1)

        ttk.Button(button_frame, text="✅ Register Employee", command=self.validate_and_submit, style="Success.TButton").grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Button(button_frame, text="💰 Calculate Salary", command=self.calculate_salary, style="Primary.TButton").grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(button_frame, text="🗑️ Clear Fields", command=self.clear_fields).grid(row=0, column=2, padx=5, sticky="ew")
        ttk.Button(button_frame, text="🚪 Exit", command=self.exit_app, style="Danger.TButton").grid(row=0, column=3, padx=5, sticky="ew")

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=(5,2))
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Configure grid weights for resizing
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Configure custom button styles
        style.configure("Success.TButton", foreground="white", background="#2e7d32", padding=8)
        style.map("Success.TButton", background=[('active', '#1b5e20')])

        style.configure("Primary.TButton", foreground="white", background="#1976d2", padding=8)
        style.map("Primary.TButton", background=[('active', '#0d47a1')])

        style.configure("Danger.TButton", foreground="white", background="#c62828", padding=8)
        style.map("Danger.TButton", background=[('active', '#b71c1c')])

        style.configure("TLabel", background="#f0f4f8", font=("Segoe UI", 10))
        style.configure("TFrame", background="#f0f4f8")
        style.configure("TLabelframe", background="#f0f4f8", font=("Segoe UI", 10, "bold"))
        style.configure("TLabelframe.Label", background="#f0f4f8", foreground="#1e3c72")

    def validate_and_submit(self):
        # Get values
        fname = self.entries["first_name"].get().strip()
        lname = self.entries["last_name"].get().strip()
        email_val = self.entries["email"].get().strip()
        dept = self.entries["department"].get().strip()

        # Empty check
        if not all([fname, lname, email_val, dept]):
            messagebox.showerror("Error", "All fields are required!")
            self.status_var.set("Error: Missing fields")
            return

        # Name validation (no numbers)
        if any(char.isdigit() for char in fname + lname):
            messagebox.showerror("Error", "Names should not contain numbers!")
            self.status_var.set("Error: Invalid name")
            return

        # Email validation
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email_val):
            messagebox.showerror("Error", "Invalid Email Format!\nExample: name@domain.com")
            self.status_var.set("Error: Invalid email")
            return

        messagebox.showinfo("Success", f"Employee {fname} {lname} registered successfully!")
        self.status_var.set(f"Employee {fname} {lname} registered")
        # Optionally clear form after successful registration
        # self.clear_fields()

    def calculate_salary(self):
        try:
            wage = float(self.daily_wage_entry.get())
            days = int(self.working_days_entry.get())

            if wage < 0 or days < 0:
                raise ValueError
            total = wage * days
            self.salary_result.config(text=f"Total Salary: ${total:,.2f}")
            self.status_var.set(f"Calculated salary: ${total:,.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid positive numbers for Daily Wage and Working Days!")
            self.status_var.set("Error: Invalid salary input")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.daily_wage_entry.delete(0, tk.END)
        self.working_days_entry.delete(0, tk.END)
        self.salary_result.config(text="Total Salary: $0.00")
        self.status_var.set("All fields cleared")

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeRegistrationSystem(root)
    root.mainloop()