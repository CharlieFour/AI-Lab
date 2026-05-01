import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import csv

# =========================
# Default Items (used if CSV missing)
# =========================
DEFAULT_ITEMS = {
    "Tea": {"price": 100, "quantity": 100},
    "Coffee": {"price": 150, "quantity": 100},
    "Burger": {"price": 300, "quantity": 100},
    "Sandwich": {"price": 250, "quantity": 100},
    "Fries": {"price": 200, "quantity": 100},
    "Juice": {"price": 180, "quantity": 100}
}

CSV_FILE = "items.csv"

# Modern Color Scheme
COLORS = {
    "bg": "#F4F6F9",
    "card": "#FFFFFF",
    "primary": "#4361EE",
    "primary_dark": "#3A56D4",
    "success": "#2EC973",
    "danger": "#E65C5C",
    "warning": "#FFB347",
    "accent": "#6C5CE7",
    "text": "#2D3436",
    "text_light": "#636E72",
    "border": "#E2E8F0"
}

class ModernBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Smart Billing System | Advanced AI Edition")
        self.root.geometry("1300x750")
        self.root.configure(bg=COLORS["bg"])
        self.root.minsize(1000, 600)

        self.center_window()

        # Load items from CSV (or create default)
        self.items = self.load_items_from_csv()

        # Variables
        self.name_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.item_var = tk.StringVar(value=list(self.items.keys())[0] if self.items else "Tea")
        self.quantity_var = tk.StringVar()
        self.price_label_var = tk.StringVar(value=f"Rs {self.items[self.item_var.get()]['price']}" if self.items else "Rs 0")

        # Build UI
        self.create_header()
        self.create_main_content()
        self.create_status_bar()

        # Bind events
        if self.items:
            self.item_combo.bind("<<ComboboxSelected>>", self.update_price_display)
            self.update_price_display()

        self.setup_styles()

    # ---------- CSV Handling ----------
    def load_items_from_csv(self):
        """Load items from CSV file. If file missing, create with defaults."""
        items = {}
        if not os.path.exists(CSV_FILE):
            self.create_default_csv()
        try:
            with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row['item_name'].strip()
                    price = int(row['price'])
                    qty = int(row['quantity'])
                    items[name] = {"price": price, "quantity": qty}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load items.csv:\n{str(e)}")
            items = DEFAULT_ITEMS.copy()
        return items

    def create_default_csv(self):
        """Create items.csv with default items and quantity 100 each."""
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["item_name", "price", "quantity"])
            for name, data in DEFAULT_ITEMS.items():
                writer.writerow([name, data["price"], data["quantity"]])

    def update_csv_quantity(self, item_name, new_quantity):
        """Update the quantity of a specific item in the CSV file."""
        rows = []
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row['item_name'] == item_name:
                    row['quantity'] = str(new_quantity)
                rows.append(row)
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def add_new_item_to_csv(self, name, price, quantity):
        """Append a new item to the CSV file."""
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, price, quantity])

    # ---------- UI Methods (unchanged except currency) ----------
    def center_window(self):
        width = 1300
        height = 750
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Modern.TCombobox",
                        fieldbackground="white",
                        background=COLORS["card"],
                        foreground=COLORS["text"],
                        arrowcolor=COLORS["primary"],
                        borderwidth=1,
                        focusthickness=0,
                        selectbackground=COLORS["primary"])
        style.map("Modern.TCombobox",
                  fieldbackground=[('readonly', 'white')])
        style.configure("Modern.TEntry",
                        fieldbackground="white",
                        borderwidth=1,
                        focuscolor=COLORS["primary"])

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=COLORS["primary"], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title_label = tk.Label(header_frame, text="SMART BILLING SYSTEM",
                               font=("Segoe UI", 24, "bold"),
                               fg="white", bg=COLORS["primary"])
        title_label.pack(side=tk.LEFT, padx=30, pady=15)

        self.time_label = tk.Label(header_frame, font=("Segoe UI", 12),
                                   fg="white", bg=COLORS["primary"])
        self.time_label.pack(side=tk.RIGHT, padx=30, pady=15)
        self.update_clock()

        subtitle = tk.Label(header_frame, text="AI-Powered Billing • Smart Discounts • Instant Receipts",
                            font=("Segoe UI", 10), fg="#B5C9FF", bg=COLORS["primary"])
        subtitle.place(x=30, y=55)

    def update_clock(self):
        now = datetime.now().strftime("%d %b %Y • %I:%M %p")
        self.time_label.config(text=now)
        self.root.after(1000, self.update_clock)

    def create_main_content(self):
        main_container = tk.Frame(self.root, bg=COLORS["bg"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        left_panel = tk.Frame(main_container, bg=COLORS["card"], relief=tk.FLAT, bd=0)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        self.apply_card_shadow(left_panel)

        right_panel = tk.Frame(main_container, bg=COLORS["card"], relief=tk.FLAT, bd=0)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.apply_card_shadow(right_panel)

        self.create_input_section(left_panel)
        self.create_receipt_section(right_panel)

    def apply_card_shadow(self, frame):
        frame.configure(highlightbackground=COLORS["border"], highlightthickness=1, highlightcolor=COLORS["border"])

    def create_input_section(self, parent):
        title = tk.Label(parent, text="🧾 BILL DETAILS", font=("Segoe UI", 16, "bold"),
                         fg=COLORS["primary"], bg=COLORS["card"])
        title.pack(anchor=tk.W, padx=25, pady=(20, 15))

        form_frame = tk.Frame(parent, bg=COLORS["card"])
        form_frame.pack(fill=tk.BOTH, padx=25, pady=10)

        self.create_modern_field(form_frame, "Customer Name", self.name_var, 0, "👤")
        self.create_modern_field(form_frame, "Contact Number", self.contact_var, 1, "📞")

        item_label = tk.Label(form_frame, text="🛒 Select Item", font=("Segoe UI", 11),
                              fg=COLORS["text"], bg=COLORS["card"])
        item_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 5))

        self.item_combo = ttk.Combobox(form_frame, textvariable=self.item_var,
                                       values=list(self.items.keys()),
                                       font=("Segoe UI", 11), state="readonly",
                                       style="Modern.TCombobox")
        self.item_combo.grid(row=2, column=1, pady=(10, 5), sticky=tk.EW)
        self.item_combo.configure(width=25)

        self.create_modern_field(form_frame, "Quantity", self.quantity_var, 3, "🔢")

        price_frame = tk.Frame(form_frame, bg=COLORS["card"])
        price_frame.grid(row=4, column=0, columnspan=2, pady=(15, 10), sticky=tk.EW)

        tk.Label(price_frame, text="💰 Item Price:", font=("Segoe UI", 11, "bold"),
                 fg=COLORS["text"], bg=COLORS["card"]).pack(side=tk.LEFT, padx=(0, 10))
        self.price_label = tk.Label(price_frame, textvariable=self.price_label_var,
                                    font=("Segoe UI", 14, "bold"),
                                    fg=COLORS["primary"], bg=COLORS["card"])
        self.price_label.pack(side=tk.LEFT)

        sep = ttk.Separator(parent, orient='horizontal')
        sep.pack(fill=tk.X, padx=25, pady=15)

        button_frame = tk.Frame(parent, bg=COLORS["card"])
        button_frame.pack(fill=tk.X, padx=25, pady=(5, 20))

        self.create_modern_button(button_frame, "✨ GENERATE RECEIPT", self.generate_bill,
                                  COLORS["success"], "#26A65B", side=tk.LEFT, padx=(0, 10))
        self.create_modern_button(button_frame, "🗑️ CLEAR", self.clear_fields,
                                  COLORS["warning"], "#E67E22", side=tk.LEFT, padx=(0, 10))
        self.create_modern_button(button_frame, "💾 SAVE RECEIPT", self.save_receipt,
                                  COLORS["primary"], COLORS["primary_dark"], side=tk.LEFT, padx=(0, 10))
        self.create_modern_button(button_frame, "➕ ADD ITEM", self.add_item,
                                  COLORS["accent"], "#5A4BCF", side=tk.LEFT, padx=(0, 10))
        self.create_modern_button(button_frame, "🚪 EXIT", self.exit_app,
                                  COLORS["danger"], "#C54B4B", side=tk.RIGHT)

        suggestion_frame = tk.Frame(parent, bg=COLORS["bg"], relief=tk.FLAT, bd=0)
        suggestion_frame.pack(fill=tk.X, padx=25, pady=(10, 20))
        tk.Label(suggestion_frame, text="🤖 AI SUGGESTION", font=("Segoe UI", 9, "bold"),
                 fg=COLORS["primary"], bg=COLORS["bg"]).pack(anchor=tk.W)
        self.suggestion_label = tk.Label(suggestion_frame, text="Select an item to see suggestion",
                                         font=("Segoe UI", 10), fg=COLORS["text_light"], bg=COLORS["bg"])
        self.suggestion_label.pack(anchor=tk.W, pady=(5, 0))
        self.update_suggestion()

    def create_modern_field(self, parent, label_text, variable, row, icon=""):
        label = tk.Label(parent, text=f"{icon} {label_text}", font=("Segoe UI", 11),
                         fg=COLORS["text"], bg=COLORS["card"])
        label.grid(row=row, column=0, sticky=tk.W, pady=(10, 5))

        entry = tk.Entry(parent, textvariable=variable, font=("Segoe UI", 11),
                         bg="white", fg=COLORS["text"], relief=tk.FLAT,
                         highlightthickness=1, highlightcolor=COLORS["primary"],
                         highlightbackground=COLORS["border"])
        entry.grid(row=row, column=1, pady=(10, 5), sticky=tk.EW, padx=(0, 20))
        entry.configure(width=30)
        return entry

    def create_modern_button(self, parent, text, command, bg_color, hover_color, side=tk.LEFT, padx=(0,0)):
        btn = tk.Button(parent, text=text, command=command,
                        font=("Segoe UI", 10, "bold"),
                        bg=bg_color, fg="white", relief=tk.FLAT,
                        padx=15, pady=8, cursor="hand2",
                        activebackground=hover_color, activeforeground="white")
        btn.pack(side=side, padx=padx)

        def on_enter(e):
            btn.config(bg=hover_color)
        def on_leave(e):
            btn.config(bg=bg_color)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def create_receipt_section(self, parent):
        title = tk.Label(parent, text="📄 RECEIPT PREVIEW", font=("Segoe UI", 16, "bold"),
                         fg=COLORS["primary"], bg=COLORS["card"])
        title.pack(anchor=tk.W, padx=20, pady=(20, 15))

        text_frame = tk.Frame(parent, bg=COLORS["card"])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.receipt_text = tk.Text(text_frame, font=("Courier New", 10),
                                    bg=COLORS["bg"], fg=COLORS["text"],
                                    relief=tk.FLAT, wrap=tk.WORD, padx=15, pady=15,
                                    highlightthickness=1, highlightbackground=COLORS["border"])
        self.receipt_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.receipt_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.receipt_text.config(yscrollcommand=scrollbar.set)

    def create_status_bar(self):
        status_frame = tk.Frame(self.root, bg=COLORS["primary"], height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        status_text = "✅ Ready | Smart Discount System Active"
        self.status_label = tk.Label(status_frame, text=status_text, font=("Segoe UI", 9),
                                     fg="white", bg=COLORS["primary"])
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)

        items_count = f"📦 Total Items: {len(self.items)}"
        count_label = tk.Label(status_frame, text=items_count, font=("Segoe UI", 9),
                               fg="white", bg=COLORS["primary"])
        count_label.pack(side=tk.RIGHT, padx=15, pady=5)

    def update_price_display(self, event=None):
        selected_item = self.item_var.get()
        if selected_item in self.items:
            price = self.items[selected_item]["price"]
            self.price_label_var.set(f"Rs {price}")
        self.update_suggestion()

    def update_suggestion(self):
        item = self.item_var.get()
        suggestions = {
            "Tea": "☕ Try Sandwich with Tea for a perfect combo!",
            "Coffee": "☕ Add a Brownie to complement your Coffee!",
            "Burger": "🍔 Add Fries & Drink to make it a meal!",
            "Sandwich": "🥪 Pair with Fresh Juice for a healthy meal!",
            "Fries": "🍟 Get a Burger combo and save 10%!",
            "Juice": "🧃 Fresh Juice goes well with Sandwich!"
        }
        suggestion = suggestions.get(item, "✨ Explore our combos for best savings!")
        self.suggestion_label.config(text=f"{suggestion}")

    def generate_receipt_text(self):
        name = self.name_var.get().strip()
        contact = self.contact_var.get().strip()
        item = self.item_var.get()
        quantity_str = self.quantity_var.get().strip()

        # Validations
        if not name or not contact or not quantity_str:
            messagebox.showerror("Error", "❌ All fields are required!", parent=self.root)
            return None
        
        if name.isdigit():
            messagebox.showerror("Error", "❌ Name cannot be numeric!", parent=self.root)
            return None

        if not contact.isdigit() or len(contact) != 11 or contact[0] != '0' or contact[1] != '3':
            messagebox.showerror("Error", "❌ Contact must be 11 digits starting with '03'!", parent=self.root)
            return None

        if not quantity_str.isdigit():
            messagebox.showerror("Error", "❌ Quantity must be numeric!", parent=self.root)
            return None

        quantity = int(quantity_str)
        if quantity <= 0:
            messagebox.showerror("Error", "❌ Quantity must be greater than zero!", parent=self.root)
            return None

        if item not in self.items:
            messagebox.showerror("Error", "❌ Invalid item selected!", parent=self.root)
            return None

        # Check stock availability
        available_qty = self.items[item]["quantity"]
        if quantity > available_qty:
            messagebox.showerror("Error", f"❌ Insufficient stock! Only {available_qty} {item}(s) available.", parent=self.root)
            return None

        # Calculations
        price = self.items[item]["price"]
        subtotal = price * quantity

        discount = 0
        discount_reason = ""
        if subtotal > 1000:
            discount = 10
            discount_reason = "Bulk purchase discount (10%)"
        elif quantity >= 5:
            discount = 5
            discount_reason = "Quantity discount (5%)"

        discount_amount = (subtotal * discount) / 100
        total = subtotal - discount_amount

        # AI suggestion
        product_suggestion = ""
        if item == "Tea":
            product_suggestion = "Smart Suggestion: Add Sandwich for a perfect combo!"
        elif item == "Burger":
            product_suggestion = "Smart Suggestion: Add Fries and save on combo!"
        elif item == "Coffee":
            product_suggestion = "Smart Suggestion: Pair with a Cookie for extra happiness!"

        # Build receipt (simple, no fixed‑width boxes)
        receipt = f"""
========================================
        SMART BILLING SYSTEM
        (AI Powered)
========================================

Date & Time : {datetime.now().strftime("%d-%m-%Y  %I:%M %p")}
Customer    : {name.upper()}
Contact     : {contact}

----------------------------------------
ITEM DETAILS
----------------------------------------
Item        : {item}
Price       : Rs {price}
Quantity    : {quantity}
----------------------------------------
Subtotal    : Rs {subtotal:.2f}

DISCOUNT INFO
{discount_reason if discount_reason else 'No discount applied'}
Discount    : {discount}%  ( - Rs {discount_amount:.2f} )
----------------------------------------
FINAL TOTAL : Rs {total:.2f}
----------------------------------------

{product_suggestion}

AI Suggestion: {self.suggestion_label.cget('text')}

Thank you for visiting!
Please come again!
========================================
"""
        # Update stock in memory and CSV
        new_qty = available_qty - quantity
        self.items[item]["quantity"] = new_qty
        self.update_csv_quantity(item, new_qty)

        return receipt

    def generate_bill(self):
        receipt = self.generate_receipt_text()
        if receipt:
            self.receipt_text.delete("1.0", tk.END)
            self.receipt_text.insert("1.0", receipt)
            self.update_status_bar("✅ Bill generated successfully!")

    def save_receipt(self):
        receipt = self.generate_receipt_text()
        if receipt:
            try:
                if not os.path.exists("receipts"):
                    os.makedirs("receipts")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"receipts/bill_{timestamp}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(receipt)
                messagebox.showinfo("Success", f"✅ Receipt saved successfully!\n📁 File: {filename}", parent=self.root)
                self.update_status_bar(f"💾 Receipt saved as {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save receipt: {str(e)}", parent=self.root)

    def clear_fields(self):
        self.name_var.set("")
        self.contact_var.set("")
        self.quantity_var.set("")
        if self.items:
            self.item_var.set(list(self.items.keys())[0])
        self.receipt_text.delete("1.0", tk.END)
        self.update_price_display()
        self.update_status_bar("🗑️ All fields cleared")

    def add_item(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ Add New Item")
        dialog.geometry("420x300")
        dialog.configure(bg=COLORS["card"])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        x = (dialog.winfo_screenwidth() // 2) - (420 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"420x300+{x}+{y}")

        tk.Label(dialog, text="Add New Item to Inventory", font=("Segoe UI", 14, "bold"),
                 fg=COLORS["primary"], bg=COLORS["card"]).pack(pady=15)

        frame = tk.Frame(dialog, bg=COLORS["card"])
        frame.pack(pady=10)

        tk.Label(frame, text="Item Name:", font=("Segoe UI", 11), bg=COLORS["card"]).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        name_entry = tk.Entry(frame, font=("Segoe UI", 11), width=25)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(frame, text="Price (Rs):", font=("Segoe UI", 11), bg=COLORS["card"]).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        price_entry = tk.Entry(frame, font=("Segoe UI", 11), width=25)
        price_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(frame, text="Quantity (stock):", font=("Segoe UI", 11), bg=COLORS["card"]).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        qty_entry = tk.Entry(frame, font=("Segoe UI", 11), width=25)
        qty_entry.grid(row=2, column=1, padx=10, pady=10)

        def save_item():
            name = name_entry.get().strip()
            price_str = price_entry.get().strip()
            qty_str = qty_entry.get().strip()

            if not name:
                messagebox.showerror("Error", "Item name cannot be empty!", parent=dialog)
                return
            if not price_str.isdigit() or int(price_str) <= 0:
                messagebox.showerror("Error", "Price must be a positive number!", parent=dialog)
                return
            if not qty_str.isdigit() or int(qty_str) < 0:
                messagebox.showerror("Error", "Quantity must be a non-negative integer!", parent=dialog)
                return

            price = int(price_str)
            qty = int(qty_str)

            if name in self.items:
                messagebox.showerror("Error", "Item already exists! Use 'Edit Item' if needed.", parent=dialog)
                return

            # Add to memory
            self.items[name] = {"price": price, "quantity": qty}
            # Add to CSV
            self.add_new_item_to_csv(name, price, qty)
            # Update dropdown
            self.item_combo['values'] = list(self.items.keys())
            self.item_var.set(name)
            self.update_price_display()
            self.update_status_bar(f"➕ Added new item: {name} (Rs {price}, stock: {qty})")
            messagebox.showinfo("Success", f"✅ Item '{name}' added successfully!", parent=dialog)
            dialog.destroy()

        btn_frame = tk.Frame(dialog, bg=COLORS["card"])
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Save Item", command=save_item, bg=COLORS["success"],
                  fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5,
                  cursor="hand2", relief=tk.FLAT).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy, bg=COLORS["danger"],
                  fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5,
                  cursor="hand2", relief=tk.FLAT).pack(side=tk.LEFT, padx=10)

    def exit_app(self):
        if messagebox.askyesno("Exit", "🚀 Are you sure you want to exit?", parent=self.root):
            self.root.destroy()

    def update_status_bar(self, message):
        self.status_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernBillingSystem(root)
    root.mainloop()