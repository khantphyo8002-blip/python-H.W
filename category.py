from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import posmain

def open_category():
    category = Tk()
    category.title("Category")
    category.geometry("800x500")
    selectid = None

    def open_posmain_box():
        category.destroy()
        posmain.open_posmain()
        
    def connect():
        return mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "admin123",
            database = "POS_db"
        )

    def save():
        cat_name = cat_name_entry.get()
        if not cat_name:
            messagebox.showerror("Error", "Please fill Category Name")
            return
        else:
            try:
                con = connect()
                cursor = con.cursor()
                query = "INSERT INTO CATEGORY (CAT_NAME) VALUES(%s)"
                cursor.execute(query, (cat_name,))
                con.commit()
                
                messagebox.showinfo("Category Creating", "You could add successfully")
                
                con.close()
                
                cat_name_entry.delete(0, END)
                cat_name_entry.focus()
                
                show_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
    def show_data():
        for item in cat_treeview.get_children():
            cat_treeview.delete(item)
        try:
            con = connect()
            cursor = con.cursor()
            query = "SELECT * FROM CATEGORY"
            cursor.execute(query)
            
            rows = cursor.fetchall()
            
            for row in rows:
                cat_treeview.insert("", END, values=row)
            
        except Exception as e:
                messagebox.showerror("Error", str(e))
                
    def selectdata(event):
        global selectid
        selectitem = cat_treeview.focus()
        data = cat_treeview.item(selectitem, "values")  
        if data: 
            selectid = data[0]
            cat_name_entry.delete(0, END)
            cat_name_entry.insert(0, data[1])
            cat_name_entry.focus()
            
    def edit():
        global selectid
        if selectid is None:
            messagebox.showwarning("Warning", "Please double in a row at first")
        #cat_name = cat_name_entry.get()
        else:
            try:
                cat_name = cat_name_entry.get()
                if cat_name == "":
                    messagebox.showwarning("Warning", "Please fill for your category to update successfuly")
                else:
                    con = connect()
                    cursor = con.cursor()
                    query = "UPDATE CATEGORY SET CAT_NAME = %s WHERE CAT_ID = %s"
                    cursor.execute(query, (cat_name, selectid,))
                    con.commit()
                    
                    messagebox.showinfo("Success", "Category update successfully")
                    
                    con.close()
                    
                    show_data()
                        
                    cat_name_entry.delete(0, END)
                    cat_name_entry.focus()
                    
                    selectid = None
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
    def delete():
        global selectid
        if selectid is None:
            messagebox.showwarning("Warning", "Please double in a row at first")
        else:
            confirm = messagebox.askyesno("Comfirm", "Are you sure you wanna to this category?")
            if confirm:
                try:
                    con = connect()
                    cursor = con.cursor()
                    query = "DELETE FROM CATEGORY WHERE CAT_ID = %s"
                    cursor.execute(query, (selectid,))
                    con.commit()
                    
                    messagebox.showinfo("Success", "Category delete successfully")
                    
                    con.close()
                    
                    show_data()
                        
                    cat_name_entry.delete(0, END)
                    cat_name_entry.focus()
                    
                    selectid = None
                    
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
    title_label = Label(category, text="Category Management", font=("arial", 20 , "bold"))
    title_label.pack(pady=10)

    input_frame = Frame(category)
    input_frame.pack(pady=10)

    label_cat_name = Label(input_frame, text="Category Name", font=("arial", 12))
    label_cat_name.grid(row=0, column=0, sticky="w", pady=(10,30), padx=10)
    cat_name_entry = Entry(input_frame, width=20, font=("arial", 12))
    cat_name_entry.grid(row=0, column=1, pady=(10,30), padx=10)

    button1 = Button(input_frame, text="Save", font=("arial", 12), height= 1, width=10, bg='lightgreen', command=save).grid(row=2, column=0, sticky="w", padx=10)
    button2 = Button(input_frame, text="Edit", font=("arial", 12), height= 1, width=10, bg='SlateBlue1', command=edit).grid(row=2, column=1)
    button3 = Button(input_frame, text="Delete", font=("arial", 12), height= 1, width=10, bg='red', command=delete).grid(row=2, column=2)

    cat_treeview = ttk.Treeview(category, columns=("ID", "Category Name"), show="headings", height=10)

    cat_treeview.heading("ID", text="ID")
    cat_treeview.heading("Category Name", text="Category Name")

    cat_treeview.column("ID", width=120)
    cat_treeview.column("Category Name", width=400)
    cat_treeview.pack(pady=10)

    cat_treeview.bind("<Double-1>", selectdata)

    btn_frame = Frame(category)
    btn_frame.pack(pady=10)
    button1 = Button(btn_frame, text="Refresh", font=("arial", 12), height= 1, width=20, bg='SlateBlue1', command=show_data).grid(row=0, column=0, padx=10)
    button2 = Button(btn_frame, text="Back to Dashboard", font=("arial", 12), height= 1, width=20, bg='gray70', command=open_posmain_box).grid(row=0, column=1, padx=10)


    show_data()
    category.mainloop()