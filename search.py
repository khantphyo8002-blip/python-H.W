from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
#import transaction

def open_invoice_data(get_id, get_date):

    invoice_data = Tk()
    invoice_data.title("Invoice Data")
    invoice_data.geometry("700x600")

    def connect():
        return mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "admin123",
            database = "POS_db"
        )
        
    def get_invoice_data():
        inv_id = get_id
        date_value = get_date
        try:
            con = connect()
            cursor = con.cursor()
            query = "SELECT D.ITEM_ID, IT.ITEM_NAME, IT.PRICE, D.QTY, D.TOTAL FROM INVOICE_DETAIL AS D , ITEMS AS IT WHERE D.ITEM_ID = IT.ITEM_ID AND D.INVID = %s;"
            cursor.execute(query, (inv_id,))
            results = cursor.fetchall() 
            if results:
                for row in item_treeview.get_children():
                    item_treeview.delete(row)
                for row in results:
                    item_treeview.insert("", "end", values=row)
                con.close()
            else:
                messagebox.showinfo("No Results", "No invoice details found for the specified invoice ID.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def set_total():
        total = 0.00
        for row in item_treeview.get_children():
            total += float(item_treeview.item(row, "values")[4])
        total_value.config(text=str(total))

    # POS_sale = Label(invoice_data, text="POS Sale", font=("Arial", 24))
    # POS_sale.pack(pady=20)

    main_frame = Frame(invoice_data)
    main_frame.pack(pady=20)

    invid_label = Label(main_frame, text="INVID:", font=("Arial", 12))
    invid_label.grid(row=0, column=0, sticky=W)
    invid_value = Label(main_frame, text=get_id, font=("Arial", 12))
    invid_value.grid(row=0, column=0)

    date_label = Label(main_frame, text="Date:", font=("Arial", 12), width=30)
    date_label.grid(row=0, column=1, pady=10, sticky=E)
    date_value = Label(main_frame, text=get_date, font=("Arial", 12))
    date_value.grid(row=0, column=1, pady=10, sticky=E)

    item_treeview = ttk.Treeview(main_frame, columns=("Item_ID", "Name", "Price", "Qty", "Total"), show="headings")

    item_treeview.heading("Item_ID", text="Item_ID")
    item_treeview.heading("Name", text="Name")
    item_treeview.heading("Price", text="Price")
    item_treeview.heading("Qty", text="Qty")
    item_treeview.heading("Total", text="Total")

    item_treeview.column("Item_ID", width=80)
    item_treeview.column("Name", width=170)
    item_treeview.column("Price", width=130, anchor=E)
    item_treeview.column("Qty", width=80, anchor=CENTER)
    item_treeview.column("Total", width=120, anchor=E)

    item_treeview.grid(row=3, column=0, columnspan=2, pady=10)

    total_label = Label(main_frame, text="Total:", font=("Arial", 15))
    total_label.grid(row=4, column=0, pady=10)

    total_value = Label(main_frame, text="0.00", font=("Arial", 15))
    total_value.grid(row=4, column=1, pady=10, sticky=E, padx=20)

    get_invoice_data()
    set_total()
    invoice_data.mainloop()
