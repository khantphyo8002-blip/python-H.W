from tkinter import *
import category
import staff
import items
import login
from tkinter import messagebox
    
def open_posmain():
    posmain = Tk()
    posmain.title("POS System Main")
    posmain.geometry("600x500")

    def open_category_box():
        posmain.destroy()
        category.open_category()
        
    def open_items_box():
        posmain.destroy()
        items.open_items()
        
    def open_staff_box():
        posmain.destroy()
        staff.open_staff()
        
    def logout():
        confrim = messagebox.askyesno("Logout", "Are you to logot?")
        if confrim:
            posmain.destroy()
            login.open_login()

    pos_title = Label(posmain, text="POS System Deshboard", font=("Arial", 18 , "bold"))
    pos_title.pack(pady=(20))

    pos_sale_btn = Button(posmain, text="POS Sale", bg="lightgreen",font=("Arial", 13), width=25, height=2, relief="ridge")
    pos_sale_btn.pack(pady=10)

    pos_manage = Label(posmain, text="Management", font=("Arial", 12))
    pos_manage.pack()

    pos_frame = Frame(posmain)
    pos_frame.pack(pady=10)

    btn_style = {"font": 7, "bg": "#C8E6C9", "width": 18, "height": 3, "bd": 1, "relief": "ridge"}

    cat_crud = Button(pos_frame, text="Category CRUD", **btn_style, command=open_category_box)
    cat_crud.grid(row=0, column=0, pady=10, padx=10)

    item_crud = Button(pos_frame, text="Item CRUD", **btn_style, command=open_items_box)
    item_crud.grid(row=0, column=1)

    staff_crud = Button(pos_frame, text="Staff CRUD", **btn_style, command=open_staff_box)
    staff_crud.grid(row=1, column=0)

    sale_crud = Button(pos_frame, text="Sale CRUD", **btn_style)
    sale_crud.grid(row=1, column=1)

    logout_btn = Button(posmain, text="Logout", bg="red", fg="black", font=("Arial", 13), bd=1, width=25, height=2, relief="ridge", command=logout)
    logout_btn.pack(pady=(20,10))

    posmain.mainloop()