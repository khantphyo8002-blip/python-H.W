from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import posmain

def open_staff():
    staff = Tk()
    staff.title("Staff")
    staff.geometry("800x500")
    
    def open_posmain_box():
        staff.destroy()
        posmain.open_posmain()

    def connect():
        return mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "admin123",
            database = "POS_db"
        )
        
    def create():
        staff_name = name_entry.get()
        staff_role = role_entry.get()
        
        if staff_name == "" or staff_role == "":
            messagebox.showerror("Error", "Please fill Staff_Name and Staff_Role")
            return
        else:
            try:
                con = connect()
                cursor = con.cursor()
                query = "INSERT INTO STAFF(STAFF_NAME, ROLE) VALUES(%s , %s)"
                cursor.execute(query,(staff_name, staff_role))                
                con.commit()
                
                messagebox.showinfo("Staff Creating", "You could add successfully")
                
                con.close()
                
                name_entry.delete(0, END)
                role_entry.delete(0, END)
                name_entry.focus()
                show_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def staffview_select_data(event):
        select_item = stafftreeview.selection()
        if select_item:
            row = stafftreeview.item(select_item)
            data = row["values"] 
            
            name_entry.delete(0, END)
            role_entry.delete(0, END)
            name_entry.focus()
            
            name_entry.insert(0, data[1])
            role_entry.insert(0, data[2])

    def update():
        select_item = stafftreeview.selection()
        if not select_item:
            messagebox.showerror("Error", "At first, you need to select")
        else:
            try:
                row = stafftreeview.item(select_item[0])
                staff_id = row["values"][0]
                
                #update_name = name_entry.get()
                #update_role = role_entry.get()
                update_name = name_entry.get()
                update_role = role_entry.get()
                if update_name == "" or update_role == "":
                    messagebox.showwarning("Warning", "Please fill for your staff to update successfully")    
                else:                
                    con = connect()
                    cursor = con.cursor()
                    query = "UPDATE STAFF SET STAFF_NAME = %s, ROLE = %s WHERE STAFF_ID = %s"
                    cursor.execute(query, (update_name, update_role, staff_id))
                    con.commit()
                    
                    messagebox.showinfo("Success", "Staff update successfully")
                    
                    show_data()
                    
                    name_entry.delete(0, END)
                    role_entry.delete(0, END)
                    name_entry.focus()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
            
    def delete():
        select_item = stafftreeview.selection()
        if not select_item:
            messagebox.showerror("Error", "At first, you need to select")
        else:
            confirm = messagebox.askyesno("Comfirm", "Are you sure you wanna to this staff?")
            if confirm:
                try:
                    row = stafftreeview.item(select_item[0])
                    staff_id = row["values"][0]
                    
                    con = connect()
                    cursor = con.cursor()
                    query = "DELETE FROM STAFF WHERE STAFF_ID = %s"
                    cursor.execute(query, (staff_id,))
                    con.commit()
                    con.close()
                    
                    messagebox.showinfo("Success", "Staff delete successfully")
                    
                    show_data()
                    
                    name_entry.delete(0, END)
                    role_entry.delete(0, END)
                    name_entry.focus()
                    
                except Exception as e:
                    messagebox.showinfo("Error", str(e))
                
    def show_data():
        # old data clear
        for item in stafftreeview.get_children():
            stafftreeview.delete(item)
                    
        try:
            con = connect()
            cursor = con.cursor()
            query = "SELECT * FROM STAFF"
            cursor.execute(query)
            
            rows = cursor.fetchall()
            
            for row in rows:
                stafftreeview.insert("", END, values=row)
            con.close()
        except Exception as e:
                messagebox.showerror("Error", str(e))

    staff_title = Label(staff, text="Staff Management", font=("arial", 20 , "bold"))
    staff_title.pack(pady=10)

    input_frame = Frame(staff)
    input_frame.pack(pady=10)

    label_name = Label(input_frame, text="Staff Name", font=("arial", 12))
    label_name.grid(row=0, column=0, sticky="w")
    name_entry = Entry(input_frame, width=20, font=("arial", 12))
    name_entry.grid(row=0, column=1, pady=10, padx=10)

    label_role = Label(input_frame, text="Role", font=("arial", 12))
    label_role.grid(row=1, column=0, sticky="w")
    role_entry = Entry(input_frame, width=20, font=("arial", 12))
    role_entry.grid(row=1, column=1, pady=(10,20))

    button1 = Button(input_frame, text="Create", font=("arial", 12), height= 1, width=10, bg='lightgreen', command=create).grid(row=2, column=0, sticky="w", padx=10)
    button2 = Button(input_frame, text="Update", font=("arial", 12), height= 1, width=10, bg='SlateBlue1', command=update).grid(row=2, column=1, sticky="w")
    button3 = Button(input_frame, text="Delete", font=("arial", 12), height= 1, width=10, bg='red', command=delete).grid(row=2, column=2)
    button4 = Button(input_frame, text="Back to Dashboard", font=("arial", 12), height= 1, width=20, bg='gray70', command=open_posmain_box).grid(row=2, column=3, padx=10)

    stafftreeview = ttk.Treeview(staff, columns=("ID", "NAME", "ROLE"), show="headings", height=20)

    stafftreeview.heading("ID", text="ID")
    stafftreeview.heading("NAME", text="NAME")
    stafftreeview.heading("ROLE", text="ROLE")

    stafftreeview.column("ID", width=80,)
    stafftreeview.column("NAME", width=300)
    stafftreeview.column("ROLE", width=250)
    stafftreeview.pack(pady=20)

    stafftreeview.bind("<Double-1>", staffview_select_data)

    show_data()
    staff.mainloop()