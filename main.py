
# ============================================================
# IMPORT LIBRARIES
# ============================================================

import tkinter as tk                  # GUI library
import pickle                         # For saving/loading data
from tkinter import ttk               # For styled widgets
from tkinter import messagebox        # For pop-up messages
from urllib.request import urlopen    # For API requests
from PIL import Image, ImageTk        # For handling images
import json                           # For parsing API data

# ============================================================
# CREATE MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("Beanorama Cafe Ordering System")
root.geometry("1200x700")
root.configure(bg="#E6E2D7")  







# ================================================================= FRAMES =================================================================

# ============================================================
# TOP FRAME (HEADER WITH LOGO AND TITLE)
# ============================================================
top_frame = tk.Frame(root, bg="#D8C3A5")
top_frame.pack(fill="x")

separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill="x")

# Load and resize logo
logo_img = Image.open("logo.png")
logo_img = logo_img.resize((90, 90))  # adjust size if needed
logo_photo = ImageTk.PhotoImage(logo_img)

# Container for logo + title
title_container = tk.Frame(top_frame, bg="#D8C3A5")
title_container.pack(pady=8)

# Logo
logo_label = tk.Label(title_container, image=logo_photo, bg="#D8C3A5")
logo_label.image = logo_photo
logo_label.pack(side="left", padx=(0, 10))

# Title
title_label = tk.Label(
    title_container,
    text="Beanorama\nCafe Ordering System",
    font=("Georgia", 22, "bold"),
    bg="#D8C3A5",
    fg="#3F1D0E"
)
title_label.pack(side="left")

# ============================================================
# MAIN FRAME (HOLDS LEFT AND RIGHT PANELS)
# ============================================================

main_frame = tk.Frame(root, bg="#E6E2D7")
main_frame.pack(fill="both", expand=True)
main_frame.pack_propagate(True)

# ============================================================
# LEFT FRAME (ORDER INPUT FORM)
# ============================================================

left_frame = tk.Frame(main_frame, bg="#E6E2D7")
left_frame.pack(side="left", fill="y", padx=15, pady=15)

left_card = tk.Frame(
    left_frame,
    bg="#E4CDB0",
    bd=0,
    highlightthickness=1,
    highlightbackground="#C2B280"
)
left_card.pack(fill="both", expand=True)

# ============================================================
# RIGHT FRAME (TABLE DISPLAY)
# ============================================================

right_frame = tk.Frame(main_frame, bg="#E6E2D7")
right_frame.pack(side="left", expand=True, fill="both", padx=15, pady=15)

right_card = tk.Frame(
    right_frame,
    bg="#F5F5F5",
    bd=0,
    highlightthickness=1,
    highlightbackground="#C2B280"
)
right_card.pack(fill="both", expand=True)

# Table columns
columns = ("Customer", "Category", "Item", "Size", "Quantity", "Total")

# Create Table
tree = ttk.Treeview(right_card, columns=columns, show="headings")

# Configure Headngs
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

order_label = tk.Label(
    left_card,
    text="Order Details",
    font=("Arial", 16, "bold"),
    bg="#E4CDB0",
    fg="#3F1D0E"
)
order_label.pack(pady=10)

# Scrollbar for table
scrollbar = tk.Scrollbar(right_card, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
scrollbar.pack(side="right", fill="y")


scrollbar.config(
    bg="#E6E2D7",
    troughcolor="#F5F5F5",
    activebackground="#C2B280"
)

style = ttk.Style()
style.configure("Treeview",
    background="#F5F5F5",
    foreground="black",
    rowheight=25,
    fieldbackground="#F5F5F5"
)

style.configure("Treeview.Heading",
    font=("Arial", 10, "bold")
)

# ============================================================
# INPUT FIELDS (FORM)
# ============================================================

# Customer Name 
customer_label = tk.Label(left_card, text="Customer Name:", bg="#E4CDB0")
customer_label.pack(anchor="w", padx=15, pady=(10, 0))

customer_entry = tk.Entry(left_card, width=30)
customer_entry.pack(padx=15, pady=6)

# Category Dropdown
category_label = tk.Label(left_card, text="Category:", bg="#E4CDB0")
category_combo = ttk.Combobox(left_card, values=[
    "Iced Coffee",
    "Milky Series",
    "Hot Coffee"
], state="readonly")
category_combo.pack(padx=15, pady=6)
category_label.pack(anchor="w", padx=15, pady=(10, 0))

# Item Dropdown
item_label = tk.Label(left_card, text="Item:", bg="#E4CDB0")
item_label.pack(anchor="w", padx=15, pady=(10, 0))

item_combo = ttk.Combobox(left_card, state="readonly")
item_combo.pack(padx=15, pady=6)

# Size Dropdown
size_label = tk.Label(left_card, text="Size:", bg="#E4CDB0")
size_label.pack(anchor="w", padx=15, pady=(10, 0))

size_combo = ttk.Combobox(left_card, values=["16oz", "22oz"], state="readonly")
size_combo.pack(padx=15, pady=6)

# Unit Price
price_label = tk.Label(left_card, text="Unit Price:", bg="#E4CDB0")
price_label.pack(anchor="w", padx=15, pady=(10, 0))

price_entry = tk.Entry(left_card)
price_entry.pack(padx=15, pady=6)

# Quantity
quantity_label = tk.Label(left_card, text="Quantity:", bg="#E4CDB0")
quantity_label.pack(anchor="w", padx=15, pady=(10, 0))

quantity_entry = tk.Entry(left_card, width=10)
quantity_entry.insert(0, "1")
quantity_entry.pack(padx=15, pady=6)

# Cash 
cash_label = tk.Label(left_card, text="Cash Tendered:", bg="#E4CDB0")
cash_label.pack(anchor="w", padx=15, pady=(10, 0))

cash_entry = tk.Entry(left_card)
cash_entry.pack(padx=15, pady=6)

# Change
change_label = tk.Label(left_card, text="Change:", bg="#E4CDB0")
change_label.pack(anchor="w", padx=15, pady=(10, 0))

change_entry = tk.Entry(left_card)
change_entry.pack(padx=15, pady=6)

# ============================================================
# MENU DATA (PYTHON COLLECTION - DICTIONARY)
# ============================================================

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


# ============================================================
# FUNCTIONS (CRUD + LOGIC)
# ============================================================

# ADD ORDER 
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
        
        save_orders()

    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter correct values.")

# DELETE FUNCTION 
def delete_order():
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showwarning("Warning", "Please select an order to delete")
        return

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this order?")
    
    if confirm:
        tree.delete(selected_item)
        save_orders()
    

# UPDATE

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
    save_orders()
    
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

# SAVE FUNCTION
def save_orders():
    with open("orders.dat", "wb") as file:
        data = []

        for item in tree.get_children():
            data.append(tree.item(item, "values"))

        pickle.dump(data, file)

# LOAD FUNCTION
def load_orders():
    try:
        with open("orders.dat", "rb") as file:
            data = pickle.load(file)

            for row in data:
                tree.insert("", "end", values=row)

    except FileNotFoundError:
        pass

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

def get_exchange_rate():
    try:
        url = 'https://www.floatrates.com/daily/usd.json'
        response = urlopen(url)
        data = json.loads(response.read())

        php_rate = data['php']['rate']

        messagebox.showinfo("Exchange Rate", f"USD to PHP: {php_rate}")

    except:
        messagebox.showerror("Error", "Failed to fetch data")

  
def on_enter(e):
    e.widget['bg'] = "#8B5A2B"

def on_leave(e):
    e.widget['bg'] = "#A2663C"


# ============================================================
# BUTTONS (USER ACTIONS)
# ============================================================

bottom_frame = tk.Frame(root, bg="#E6E2D7", height=70)
bottom_frame.pack(side="bottom", fill="x")

bottom_frame.pack_propagate(False)

button_frame = tk.Frame(bottom_frame, bg="#E6E2D7")
button_frame.pack(pady=5)

for i in range(5):
    button_frame.columnconfigure(i, weight=1)

btn_style = {
    "bg": "#A2663C",
    "fg": "white",
    "height": 2,
    "font": ("Arial", 11, "bold"),  # slightly bigger
    "cursor": "hand2",
    "bd": 0,
    "activebackground": "#8B5A2B"
}

add_button = tk.Button(
    button_frame,
    text="Add Order",
    command=add_order,
    **btn_style
)
add_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

delete_button = tk.Button(
    button_frame,
    text="Delete Order",
    command=delete_order,
    **btn_style
)
delete_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

update_button = tk.Button(
    button_frame,
    text="Update Order",
    command=update_order,
    **btn_style
)
update_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

api_button = tk.Button(
    button_frame,
    text="Get USD to PHP",
    command=get_exchange_rate,
    **btn_style
)
api_button.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

save_button = tk.Button(
    button_frame,
    text="Save",
    command=save_orders,
    **btn_style
)
save_button.grid(row=0, column=4, padx=10, pady=5, sticky="ew")




# ================================================================= BINDS =================================================================
category_combo.bind("<<ComboboxSelected>>", update_items)
item_combo.bind("<<ComboboxSelected>>", update_price)
size_combo.bind("<<ComboboxSelected>>", update_price)
quantity_entry.bind("<KeyRelease>", calculate_total)
cash_entry.bind("<KeyRelease>", calculate_total)
tree.bind("<<TreeviewSelect>>", load_selected)

add_button.bind("<Enter>", on_enter)
add_button.bind("<Leave>", on_leave)

delete_button.bind("<Enter>", on_enter)
delete_button.bind("<Leave>", on_leave)

update_button.bind("<Enter>", on_enter)
update_button.bind("<Leave>", on_leave)

api_button.bind("<Enter>", on_enter)
api_button.bind("<Leave>", on_leave)
    
# ============================================================
# LOAD DATA AND RUN PROGRAM
# ============================================================
load_orders()
root.mainloop()