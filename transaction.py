import tkinter as tk  
from tkinter import messagebox 
#for mac os user  
#from tkmacosx import Button as MacButton  
#for treeview module ttk import 
from tkinter import ttk 
import mysql.connector 
from datetime import date 
from tkcalendar import DateEntry 
import search

def connect():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "admin123",
        database = "POS_db"
    )  
    
def search_data():
    search_date = date_entry.get()
    if not search_date:
        messagebox.showerror("Error", "Please select a date to search.")
        return
    else:
        try:
            con = connect()
            cursor = con.cursor()
            query = "SELECT I.INVID, I.TOTAL_AMMOUNT, INVOICE_DATE, S.STAFF_NAME FROM INVOICE AS I , STAFF AS S WHERE I.STAFF_ID = S.STAFF_ID AND INVOICE_DATE = %s;"
            cursor.execute(query, (search_date,))
            results = cursor.fetchall() 
            if results:
                for row in invoicetransation.get_children():
                    invoicetransation.delete(row)
                for row in results:
                    invoicetransation.insert("", "end", values=row)
            else:
                messagebox.showinfo("No Results", "No transactions found for the selected date.")
            con.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def clear():
    date_entry.set_date(date.today())
    for row in invoicetransation.get_children():
        invoicetransation.delete(row)

def get_data(event):
    selected_item = invoicetransation.focus()
    if selected_item:
        item_values = invoicetransation.item(selected_item, "values")
        global invoice_id, date_value
        invoice_id = item_values[0]
        date_value = item_values[2]
        search.open_invoice_data(invoice_id, date_value)

root=tk.Tk() 
style = ttk.Style() 
style.theme_use('clam') 
root.title("POS System Transaction Form") 
root.geometry("800x500") 

tk.Label(root,text="Sale Transaction Report",font=("Arial",20,"bold"),pady=20).pack() 

input_frame = tk.Frame(root) 
input_frame.pack(pady=5,anchor='w') 

lblsearch=tk.Label(input_frame,text="Search By Date:",font=("Arial", 13, "bold")) 
lblsearch.grid(row=0,column=0,pady=5,padx=20,sticky='w') 

date_entry = DateEntry(input_frame, font=("Arial", 12), width=20, date_pattern='yyyy-mm-dd',background='darkblue',foreground='white',borderwidth=2) 

#date_entry.drop_down() 
date_entry.grid(row=0,column=1,pady=5,padx=20,sticky='w') 

#date_entry.bind("<Button-1>", open_cal) 
date_entry.bind("<Button-1>") 

btnsearch=tk.Button(input_frame,text="Search",width=10,bg="#D0F4D1",height=1, command=search_data) 
btnsearch.grid(row=0,column=2,pady=5,padx=5,sticky='w') 

btnclear=tk.Button(input_frame,text="Clear",width=10,bg="#D0F4D1",height=1, command=clear) 
btnclear.grid(row=0,column=3,pady=5,padx=5,sticky='w') 

invoicetransation = ttk.Treeview(input_frame,columns=("Invoice_ID","Amount","Invocie_Date","Staff"),show="headings",height=20) 

invoicetransation.heading("Invoice_ID",text="Invoice_ID") 
invoicetransation.heading("Amount",text="Amount") 
invoicetransation.heading("Invocie_Date",text="Invocie_Date") 
invoicetransation.heading("Staff",text="Staff") 

invoicetransation.column("Invoice_ID",width=80) 
invoicetransation.column("Amount",width=200) 
invoicetransation.column("Invocie_Date",width=100) 
invoicetransation.column("Staff",width=100) 
invoicetransation.bind("<Double-1>", get_data)

invoicetransation.grid(row=1,column=0,columnspan=4,pady=5,padx=20,sticky='ew') 

root.mainloop()