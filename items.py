from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import posmain

def open_items():
    items = Tk()
    items.title("Items System")
    items.geometry("800x500")
    select_id = None
    
    def open_posmain_box():
        items.destroy()
        posmain.open_posmain()

    def connect():
        return mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "admin123",
            database = "POS_db"
        )


    def show_category_data():
        global category_dict
        category_dict = {}
        try:
            con = connect()
            cursor = con.cursor()
            query = "SELECT * FROM CATEGORY"
            cursor.execute(query)
            
            rows = cursor.fetchall()
            
            category_id_list = []
            category_list = []
            
            for row in rows:
                category_id = row[0]
                category_name = row[1]
                
                category_dict[category_name] = category_id
                category_list.append(category_name)
                
            items_category_combo["values"] = category_list
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_items():
        items_name = items_name_entry.get()
        items_price = items_price_entry.get()
        items_barcode = items_barcode_entry.get()
        category_name = items_category_combo.get()
        
        if category_name == "Select Category" or category_name == "":
            messagebox.showwarning("Warning", "Please, At first, choose category")
            return
        elif items_name == "" or items_price == "" or items_barcode == "":
            messagebox.showwarning("Warning", "Please fill for your item detatily")
            return
        else:
            #messagebox.showinfo("OK", "this is ok")
            category_id = category_dict[category_name] 
            try:
                con = connect()
                cursor = con.cursor()
                query = "INSERT INTO ITEMS (ITEM_NAME, PRICE, BARCODE, CAT_ID) VALUES(%s, %s, %s, %s);"
                cursor.execute(query,(items_name, items_price, items_barcode, category_id))                
                con.commit()
                
                messagebox.showinfo("Staff Creating", "You could add successfully")
                
                con.close()
                
                items_name_entry.delete(0, END)
                items_price_entry.delete(0, END)
                items_barcode_entry.delete(0, END)
                items_category_combo.set("Select Category")
                items_name_entry.focus()
                
                show_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                return
            
    def selectdata(event):
        global select_id
        selectitem = items_treeview.focus()
        data = items_treeview.item(selectitem, "values")
        if data:
            select_id = data[0]
            items_name_entry.delete(0, END)
            items_name_entry.insert(0, data[1])
            items_name_entry.focus()
            
            items_price_entry.delete(0, END)
            items_price_entry.insert(0, data[2])
            
            items_barcode_entry.delete(0, END)
            items_barcode_entry.insert(0, data[3])
            
            items_category_combo.set(data[4])
            
    def update():
        global select_id
        if select_id is None:
            messagebox.showwarning("Warning", "Please double in a row at first")
        else:
            try:
                items_name = items_name_entry.get()
                items_price = items_price_entry.get()
                items_barcode = items_barcode_entry.get()
                category_name = items_category_combo.get()
        
                category_id = category_dict[category_name]  
                
                con = connect()
                cursor = con.cursor()
                query = "UPDATE ITEMS SET ITEM_NAME = %s, PRICE = %s, BARCODE = %s, CAT_ID = %s WHERE ITEM_ID = %s"
                cursor.execute(query,(items_name, items_price, items_barcode, category_id, select_id))
                con.commit()
                
                messagebox.showinfo("Success", "Item updat successfully")
                
                con.close()
                
                items_name_entry.delete(0, END)
                items_price_entry.delete(0, END)
                items_barcode_entry.delete(0, END)
                items_category_combo.set("Select Category")
                items_name_entry.focus()
                
                select_id = None
                
                show_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
    def delete():
        global select_id
        if select_id is None:
            messagebox.showwarning("Warning", "Please double in a row at first")
        else:
            confirm = messagebox.askyesno("Comfirm", "Are you sure you wanna to this category?")
            if confirm:
                try:
                    con = connect()
                    cursor = con.cursor()
                    query = "DELETE FROM ITEMS WHERE ITEM_ID = %s"
                    cursor.execute(query,(select_id,))
                    con.commit()
                        
                    messagebox.showinfo("Success", "Item delete successfully")
                        
                    con.close()
                        
                    items_name_entry.delete(0, END)
                    items_price_entry.delete(0, END)
                    items_barcode_entry.delete(0, END)
                    items_category_combo.set("Select Category")
                    items_name_entry.focus()
                    
                    select_id = None
                        
                    show_data()
                except Exception as e:
                        messagebox.showerror("Error", str(e)) 
        
    def show_data():
        for item in items_treeview.get_children():
            items_treeview.delete(item)
        try:
            con = connect()
            cursor = con.cursor()
            query = "SELECT I.ITEM_ID, I.ITEM_NAME, I.PRICE, I.BARCODE, C.CAT_NAME FROM ITEMS AS I LEFT JOIN CATEGORY AS C ON C.CAT_ID = I.CAT_ID"
            cursor.execute(query)
            
            rows = cursor.fetchall()
            
            for row in rows:
                items_treeview.insert("", END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

    items_title = Label(items, text="Items Management", font=("arial", 20 , "bold"))
    items_title.pack(pady=10)

    input_frame = Frame(items)
    input_frame.pack(pady=10)

    #row=0
    items_name = Label(input_frame, text="Item Name", font=("arial", 12))
    items_name.grid(row=0, column=0, sticky="w", pady=25)
    items_name_entry = Entry(input_frame, width=20, font=("arial", 12))
    items_name_entry.grid(row=0, column=1, padx=20)
    items_price = Label(input_frame, text="Price", font=("arial", 12))
    items_price.grid(row=0, column=2, sticky="w")
    items_price_entry = Entry(input_frame, width=22, font=("arial", 12))
    items_price_entry.grid(row=0, column=3, padx=20)

    #row=1
    items_barcode = Label(input_frame, text="Barcode", font=("arial", 12))
    items_barcode.grid(row=1, column=0, sticky="w", pady=(0,25))
    items_barcode_entry = Entry(input_frame, width=20, font=("arial", 12))
    items_barcode_entry.grid(row=1, column=1, pady=(0,25))
    items_category = Label(input_frame, text="Category", font=("arial", 12))
    items_category.grid(row=1, column=2, sticky="w", pady=(0,25))
    items_category_combo = ttk.Combobox(input_frame, values=[], state="readonly", font=("arial", 12))
    items_category_combo.grid(row=1, column=3, pady=(0,25))
    items_category_combo.set("Select Category")

    #row=2
    button1 = Button(input_frame, text="Create", font=("arial", 12), height= 1, width=10, bg='lightgreen', command=create_items).grid(row=2, column=0)
    button2 = Button(input_frame, text="Update", font=("arial", 12), height= 1, width=10, bg='SlateBlue1', command=update).grid(row=2, column=1, sticky="w", padx=20)
    button3 = Button(input_frame, text="Delete", font=("arial", 12), height= 1, width=10, bg='red', command=delete).grid(row=2, column=2)
    button4 = Button(input_frame, text="Back to Dashboard", font=("arial", 12), height= 1, width=20, bg='gray70', command=open_posmain_box).grid(row=2, column=3, padx=20)

    items_treeview = ttk.Treeview(items, columns=("ID", "Name", "Price", "Barcode", "Category"), show="headings", height=20)

    items_treeview.heading("ID", text="ID")
    items_treeview.heading("Name", text="Name")
    items_treeview.heading("Price", text="Price")
    items_treeview.heading("Barcode", text="Barcode")
    items_treeview.heading("Category", text="Category")

    items_treeview.column("ID", width=100)
    items_treeview.column("Name", width=250)
    items_treeview.column("Price", width=120)
    items_treeview.column("Barcode", width=100)
    items_treeview.column("Category", width=150)
    items_treeview.pack(pady=10)

    items_treeview.bind("<Double-1>", selectdata)


    show_data()
    show_category_data()
    items.mainloop()