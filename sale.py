from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import random
import datetime

sale = Tk()
sale.title("Sale")
sale.geometry("1000x700")
select_id = None

def connect():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "admin123",
        database = "POS_db"
    )  
    
def show_data():
    for item in item_treeview.get_children():
        item_treeview.delete(item)
    try:
        con = connect()
        cursor = con.cursor()
        query = "SELECT I.ITEM_ID, I.ITEM_NAME, I.PRICE, I.BARCODE FROM ITEMS AS I "
        cursor.execute(query)
            
        rows = cursor.fetchall()
            
        for row in rows:
            item_treeview.insert("", END, values=row)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return
    
def show_staff_data():
        global staff_dict
        staff_dict = {}
        try:
            con = connect()
            cursor = con.cursor()
            query = "SELECT * FROM STAFF"
            cursor.execute(query)
            
            rows = cursor.fetchall()
            
            staff_id_list = []
            staff_list = []
            
            for row in rows:
                staff_id = row[0]
                staff_name = row[1]
                
                staff_dict[staff_name] = staff_id
                staff_list.append(staff_name)
                
            staff_combo["values"] = staff_list
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

def add_by_code():
    get_barcode = barcode_entry.get().strip()
    if not get_barcode:
        messagebox.showerror("Error", "Please enter a barcode.")
        return
    for item in item_treeview.get_children():
        value = item_treeview.item(item, "values")
        
        barcode = value[3]
        name = value[1]
        price = float(value[2])
        
        if barcode == get_barcode:
            for card_item in card_treeview.get_children():
                card_value = card_treeview.item(card_item, "values")
                if card_value[0] == value[0]:  # Check if item ID matches
                    current_qty = int(card_value[3])
                    new_qty = current_qty + 1
                    new_total = price * new_qty
                    card_treeview.item(card_item, values=(value[0], name, price, new_qty, new_total))
                    set_total()
                    return
            
            # If item is not already in the card, add it as a new entry
            card_treeview.insert("", END, values=(value[0], name, price, 1, price))
            barcode_entry.delete(0, END)
            set_total()
            return
    messagebox.showerror("Error", "Item not found for the given barcode.")   
            
def card_code_random():
    random_code = random.randint(100000, 999999)
    card_no.config(text=str(random_code))
def card_code():
    #card_number = int(datetime.datetime.now().timestamp())
    card_number = str(datetime.datetime.now().strftime("%d%m%Y%H%M%S"))
    card_no.config(text=str(card_number))

"""def set_total():
    total = 0
    for item in card_treeview.get_children():
        value = card_treeview.item(item, "values")
        total += float(value[4])
    total_no.config(text=str(total))"""
def set_total():
    total = 0
    for item in card_treeview.get_children():
        value = card_treeview.item(item, "values")
        total += float(value[4])
    total_no.config(text=f"{total:.2f}")

def select_cart_item(event):
    global select_id
    select_item = card_treeview.selection()
    if select_item:
        row = card_treeview.item(select_item)
        data = row["values"]
        select_id = data[0]

def add_qty():
    if select_id is None:
        messagebox.showerror("Error", "Please select an item from the card.")
        return
    for item in card_treeview.get_children():
        value = card_treeview.item(item, "values")
        if str(value[0]) == str(select_id):
            current_qty = int(value[3])
            new_qty = current_qty + 1
            new_total = float(value[2]) * new_qty
            card_treeview.item(item, values=(value[0], value[1], value[2], new_qty, new_total))
            set_total()
            return

def reduce_qty():
    if select_id is None:
        messagebox.showerror("Error", "Please select an item from the card.")
        return
    for item in card_treeview.get_children():
        value = card_treeview.item(item, "values")
        if str(value[0]) == str(select_id):
            current_qty = int(value[3])
            if current_qty > 1:
                new_qty = current_qty - 1
                new_total = float(value[2]) * new_qty
                card_treeview.item(item, values=(value[0], value[1], value[2], new_qty, new_total))
                set_total()
                return
    
def remove_item():
    if select_id is None:
        messagebox.showerror("Error", "Please select an item from the card.")
        return
    else:
        confrim = messagebox.askyesno("Confirm", "Are you sure you want to remove this item from the card?")
        if confrim:
            for item in card_treeview.get_children():
                value = card_treeview.item(item, "values")
                if str(value[0]) == str(select_id):
                    card_treeview.delete(item)
                    set_total()
                    return

def clear_item():
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear the card?")
    if confirm:
        for item in card_treeview.get_children():
            card_treeview.delete(item)
    set_total()

def checkout():
    if not card_treeview.get_children():
        messagebox.showerror("Error", "The card is empty. Please add items before checkout.")
        return
    elif staff_combo.get() == "Select Staff":
        messagebox.showerror("Error", "Please select a staff member before checkout.")
        return
    else:
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to checkout?")
        if confirm:
            card_number = int(card_no.cget("text"))
            total = float(total_no.cget("text"))
            staff_name = staff_combo.get()
            staff_id = staff_dict.get(staff_name)
            date_time = datetime.datetime.now().strftime("%Y-%m-%d")
            
            try:
                con = connect()
                cursor = con.cursor()
                query = "INSERT INTO INVOICE (INVID, INVOICE_DATE, TOTAL_AMMOUNT, STAFF_ID) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (card_number, date_time, total, staff_id))
                
                query1 = "INSERT INTO INVOICE_DETAIL (INVID, ITEM_ID, QTY, TOTAL) VALUES (%s, %s, %s, %s)"
                for item in card_treeview.get_children():
                    value = card_treeview.item(item, "values")
                    item_id = value[0]
                    quantity = int(value[3])
                    total_price = float(value[4])
                    cursor.execute(query1, (card_number, item_id, quantity, total_price))
                con.commit()
                messagebox.showinfo("Success", "Checkout successful.")
                con.close()
                for item in card_treeview.get_children():
                    card_treeview.delete(item)
                staff_combo.set("Select Staff")
                set_total()
                card_code()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
def print_receipt():
    messagebox.showinfo("Print", "Receipt printed successfully.")
    
POS_sale = Label(sale, text="POS Sale", font=("Arial", 24))
POS_sale.pack(pady=20)

main_frame = Frame(sale)
main_frame.pack(pady=20)

barcode_search = Label(main_frame, text="Barcode Search:", font=("Arial", 14))
barcode_search.grid(row= 0, column= 0, sticky=W)

barcode_entry = Entry(main_frame, font=("Arial", 12), width=30)
barcode_entry.grid(row=1, column=0, pady=10, sticky=W)

Button(main_frame, text="Search", font=("Arial", 11), bg="seagreen1", width=14, command= add_by_code).grid(row=1, column=1, padx=10, pady=10)

items_label = Label(main_frame, text="Items:", font=("Arial", 14))
items_label.grid(row=2, column=0, pady=5, sticky=W)

item_treeview = ttk.Treeview(main_frame, columns=("ID", "Name", "Price", "Barcode"), show="headings", height=9)

item_treeview.heading("ID", text="ID")
item_treeview.heading("Name", text="Name")
item_treeview.heading("Price", text="Price")
item_treeview.heading("Barcode", text="Barcode")

item_treeview.column("ID", width=50)
item_treeview.column("Name", width=150)
item_treeview.column("Price", width=100)
item_treeview.column("Barcode", width=150)

item_treeview.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

#card section
# --- Card Section ကို Frame တစ်ခုထဲ စုထည့်မယ် ---
card_frame = Frame(main_frame)
card_frame.grid(row=0, column=3, rowspan=4, columnspan=4, sticky=NW, padx=10) # row 0 ကနေ စယူမယ်
#card = Label(main_frame, text="Card:", font=("Arial", 14))
#card.grid(row=0, column=3, sticky=W, padx=10)
# Card Label
card_label = Label(card_frame, text="Card:", font=("Arial", 14))
card_label.pack(side=TOP, anchor=W)

card_no = Label(main_frame, text=":", font=("Arial", 12))
card_no.grid(row=0, column=5, sticky=E, padx=10)

card_treeview = ttk.Treeview(card_frame, columns=("ID", "Name", "Price", "Qty", "Total"), show="headings" ,height=12)
card_treeview.heading("ID", text="ID")
card_treeview.heading("Name", text="Name")
card_treeview.heading("Price", text="Price")
card_treeview.heading("Qty", text="Qty")
card_treeview.heading("Total", text="Total")

card_treeview.column("ID", width=50)
card_treeview.column("Name", width=150)
card_treeview.column("Price", width=100)
card_treeview.column("Qty", width=50)
card_treeview.column("Total", width=100)
card_treeview.bind("<<TreeviewSelect>>", select_cart_item)

#card_treeview.grid(row=1, column=3, rowspan=3, columnspan=4, padx=10)
card_treeview.pack(side=TOP, pady=10)

#card button section
bottom_frame = Frame(main_frame)
bottom_frame.grid(row=4, column=2, columnspan=4)

qty_plus = Button(bottom_frame, text="+ Qty", font=("Arial", 10), width=7, bg="cyan1", command=add_qty)
qty_plus.pack(side=LEFT, padx=10)
qty_minus = Button(bottom_frame, text="- Qty", font=("Arial", 10), width=7, bg="yellow3", command=reduce_qty)
qty_minus.pack(side=LEFT, padx=10)
remove = Button(bottom_frame, text="Remove", font=("Arial", 10), width=14, bg="royalblue1", command=remove_item)
remove.pack(side=LEFT, padx=10)
clear_card = Button(bottom_frame, text="Clear Card", font=("Arial", 10), width=15, bg="red", command=clear_item)
clear_card.pack(side=LEFT, padx=10)

#total section
total_label = Label(main_frame, text="TOTAL", font=("Arial", 13))
total_label.grid(row=5, column=3, sticky=W, pady=20, padx=10)
total_no = Label(main_frame, text="0.00", font=("Arial", 13))
total_no.grid(row=5, column=5, sticky=E, pady=20)

#staff section
staff = Label(main_frame, text="Staff", font=("Arial", 13))
staff.grid(row=6, column=3, sticky=W, padx=10)
staff_combo = ttk.Combobox(main_frame, values=[], state="readonly", font=("arial", 12))
staff_combo.grid(row=6, column=5, sticky=E, pady=10)
staff_combo.set("Select Staff")

Button(main_frame, text="Checkout", font=("Arial", 12), bg="green", fg="white", width=15, command=checkout).grid(row=7, column=3, sticky=W, pady=10)
Button(main_frame, text="Print", font=("Arial", 12), bg="orange", fg="white", width=15, command=print_receipt).grid(row=7, column=5, sticky=E)

show_staff_data()
show_data()
card_code()
sale.mainloop()