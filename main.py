import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("Beanorama Cafe Ordering System")
root.geometry("1200x700")
root.configure(bg="#E6E2D7")  # Milk color



# ========== FRAMES ==========

# Top Frame (Title)
top_frame = tk.Frame(root, bg="#E6E2D7", height=80)
top_frame.pack(fill="x")

title_label = tk.Label(
    top_frame,
    text="Beanorama\nCafe Ordering System",
    font=("Georgia", 24, "bold"),
    bg="#E6E2D7",
    fg="#3F1D0E"  # Coffee color
)
title_label.pack(pady=10)

# Left Frame (Order Details)
left_frame = tk.Frame(root, bg="#E4CDB0", width=400)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

order_label = tk.Label(
    left_frame,
    text="Order Details",
    font=("Arial", 16, "bold"),
    bg="#E4CDB0",
    fg="#3F1D0E"
)
order_label.pack(pady=10)

# Right Frame (Summary + Table)
right_frame = tk.Frame(root, bg="#E4CDB0")
right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

columns = ("Customer", "Category", "Item", "Size", "Quantity", "Total")

tree = ttk.Treeview(right_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(fill="both", expand=True)

# Bottom Frame (Buttons)
bottom_frame = tk.Frame(root, bg="#E6E2D7", height=80)
bottom_frame.pack(fill="x", side="bottom")

button_frame = tk.Frame(bottom_frame, bg="#E6E2D7")
button_frame.pack(pady=10, anchor="center")

button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2, weight=1)

# Customer Name Field
customer_label = tk.Label(left_frame, text="Customer Name:", bg="#E4CDB0")
customer_label.pack(anchor="w", padx=10)

customer_entry = tk.Entry(left_frame, width=30)
customer_entry.pack(padx=10, pady=5)

# Category Dropdown
category_label = tk.Label(left_frame, text="Category:", bg="#E4CDB0")
category_label.pack(anchor="w", padx=10)

category_combo = ttk.Combobox(left_frame, values=[
    "Iced Coffee",
    "Milky Series",
    "Hot Coffee"
], state="readonly")
category_combo.pack(padx=10, pady=5)

# Item Dropdown
item_label = tk.Label(left_frame, text="Item:", bg="#E4CDB0")
item_label.pack(anchor="w", padx=10)

item_combo = ttk.Combobox(left_frame, state="readonly")
item_combo.pack(padx=10, pady=5)

# Size Dropdown
size_label = tk.Label(left_frame, text="Size:", bg="#E4CDB0")
size_label.pack(anchor="w", padx=10)

size_combo = ttk.Combobox(left_frame, values=["16oz", "22oz"], state="readonly")
size_combo.pack(padx=10, pady=5)

price_label = tk.Label(left_frame, text="Unit Price:", bg="#E4CDB0")
price_label.pack(anchor="w", padx=10)

price_entry = tk.Entry(left_frame)
price_entry.pack(padx=10, pady=5)

# Quantity
quantity_label = tk.Label(left_frame, text="Quantity:", bg="#E4CDB0")
quantity_label.pack(anchor="w", padx=10)

quantity_entry = tk.Entry(left_frame, width=10)
quantity_entry.insert(0, "1")
quantity_entry.pack(padx=10, pady=5)

# Cash + Change
cash_label = tk.Label(left_frame, text="Cash Tendered:", bg="#E4CDB0")
cash_label.pack(anchor="w", padx=10)

cash_entry = tk.Entry(left_frame)
cash_entry.pack(padx=10, pady=5)

change_label = tk.Label(left_frame, text="Change:", bg="#E4CDB0")
change_label.pack(anchor="w", padx=10)

change_entry = tk.Entry(left_frame)
change_entry.pack(padx=10, pady=5)

menu = {
    "Iced Coffee": {
        "Americano": {"16oz": 55, "22oz": 70},
        "Cafe Latte": {"16oz": 55, "22oz": 70},
        "French Vanilla": {"16oz": 69, "22oz": 79}
    },
    "Milky Series": {
        "Matcha": {"16oz": 65, "22oz": 75},
        "Chocolate": {"16oz": 65, "22oz": 75},
        "Oreo": {"16oz": 69, "22oz": 85}
    },
    "Hot Coffee": {
        "Cafe Americano": {"Regular": 45},
        "Cafe Latte": {"Regular": 50}
    }
}

orders = []

def update_items(event):
    selected_category = category_combo.get()
    items = list(menu.get(selected_category, {}).keys())
    item_combo['values'] = items
    
def update_price(event):
    category = category_combo.get()
    item = item_combo.get()
    size = size_combo.get()

    try:
        price = menu[category][item][size]
        price_entry.delete(0, tk.END)
        price_entry.insert(0, str(price))
    except:
        pass

# CALCULATE FUNCTION
def calculate_total(event=None):
    try:
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
        total = price * quantity

        cash = float(cash_entry.get())
        change = cash - total

        change_entry.delete(0, tk.END)

        if change < 0:
            change_entry.insert(0, "Insufficient")
        else:
            change_entry.insert(0, str(change))

    except ValueError:
        return

# ADD ORDER FUNCTION
def add_order():
    try:
        customer = customer_entry.get()
        category = category_combo.get()
        item = item_combo.get()
        size = size_combo.get()

        # Validation 
        if not all([customer, category, item, size]):
            messagebox.showwarning("Input Error", "Please complete all fields!")
            return

        quantity = int(quantity_entry.get())
        price = float(price_entry.get())

        total = price * quantity
        cash = float(cash_entry.get())

        # Cash Validation 
        if cash < total:
            messagebox.showerror("Error", "Insufficient cash!")
            return

        order = [customer, category, item, size, quantity, total]
        orders.append(order)

        tree.insert("", "end", values=order)
        clear_fields()

        print("Order added:", order)

    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter correct values.")

# DELETE FUNCTION [ CRUD ]
def delete_order():
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showwarning("Warning", "Please select an order to delete")
        return

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this order?")
    
    if confirm:
        tree.delete(selected_item)
    

# LOAD FUNCTION [ CRUD ]
def load_selected(event):
    selected = tree.selection()

    if selected:
        values = tree.item(selected, "values")

        customer_entry.delete(0, tk.END)
        customer_entry.insert(0, values[0])

        category_combo.set(values[1])
        item_combo.set(values[2])
        size_combo.set(values[3])

        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, values[4])

        price_entry.delete(0, tk.END)
        price_entry.insert(0, float(values[5]) / int(values[4]))

# UPDATE ORDER [ CRUD ]
def update_order():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select an order to update")
        return

    # GET VALUES FIRST
    customer = customer_entry.get()
    category = category_combo.get()
    item = item_combo.get()
    size = size_combo.get()

    # VALIDATION AFTER getting values
    if not all([customer, category, item, size]):
        messagebox.showwarning("Input Error", "Please complete all fields!")
        return

    quantity = quantity_entry.get()
    total = float(price_entry.get()) * int(quantity)

    tree.item(selected, values=(
        customer, category, item, size, quantity, total
    ))

    messagebox.showinfo("Success", "Order updated successfully!")
    
def clear_fields():
    customer_entry.delete(0, tk.END)
    category_combo.set("")
    item_combo.set("")
    size_combo.set("")
    price_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    quantity_entry.insert(0, "1")
    cash_entry.delete(0, tk.END)
    change_entry.delete(0, tk.END)

# BUTTONS
add_button = tk.Button(
    button_frame,
    text="Add Order",
    bg="#A2663C",
    fg="white",
    height=2,
    font=("Arial", 10, "bold"),
    cursor="hand2",
    command=add_order
)
add_button.grid(row=0, column=0, padx=20)

delete_button = tk.Button(
    button_frame,
    text="Delete Order",
    bg="#A2663C",
    fg="white",
    height=2,
    font=("Arial", 10, "bold"),
    cursor="hand2",
    command=delete_order
)
delete_button.grid(row=0, column=1, padx=20)

update_button = tk.Button(
    button_frame,
    text="Update Order",
    bg="#A2663C",
    fg="white",
    height=2,
    font=("Arial", 10, "bold"),
    cursor="hand2",
    command=update_order
)
update_button.grid(row=0, column=2, padx=20)

# Binds    
category_combo.bind("<<ComboboxSelected>>", update_items)
item_combo.bind("<<ComboboxSelected>>", update_price)
size_combo.bind("<<ComboboxSelected>>", update_price)
quantity_entry.bind("<KeyRelease>", calculate_total)
cash_entry.bind("<KeyRelease>", calculate_total)
tree.bind("<<TreeviewSelect>>", load_selected)
    
    
# Runs the app
root.mainloop()