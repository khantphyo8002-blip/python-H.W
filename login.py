from tkinter import *
from tkinter import messagebox
import mysql.connector
import posmain

def open_login():
    login = Tk()
    login.title("User Login")
    login.geometry("600x500")

    def connectdb():
        return mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "admin123",
            database = "POS_db"
        )

    def login_action():
        username = user_entry.get()
        password = pass_entry.get()
        
        if username == "" and password == "":
            messagebox.showwarning("Warning", "Please fill username and password")
        else:
            try:
                con = connectdb()
                cursor = con.cursor()
                query = "SELECT * FROM USERS WHERE USER_NAME = %s AND PASSWORDS = %s"
                cursor.execute(query, (username, password))
                result = cursor.fetchone()
                if result:
                    messagebox.showinfo("Login", "Login Successful")
                    login.destroy()
                    posmain.open_posmain()
                else:
                    messagebox.showerror("Login Failed", "Your Username and Password are wrong")                
            except Exception as e:
                messagebox.showerror("Error", str(e))
            
        """else:
            messagebox.showerror("Login Failed", "Invalid username or password")"""

    label_title = Label(login, text="POS System Login", font=("Arial", 20, "bold"))
    label_title.pack(pady=20)

    frame = Frame(login)
    frame.pack(pady=10)

    user_label = Label(frame, text="User Name", font=("Arial", 12))
    user_label.grid(row=0, column=0)

    pass_label = Label(frame, text="Password", font=("Arial", 12))
    pass_label.grid(row=1 , column=0)

    user_entry = Entry(frame, width=27, font=("Arial", 12))
    user_entry.grid(row=0, column=1, pady=10, padx=10)

    pass_entry = Entry(frame, width=27,font=("Arial", 12), show="*")
    pass_entry.grid(row=1, column=1, pady=10, padx=10)

    button = Button(login, text="Login", bg="green", width=20, height=1, font=("Arial", 12), command=login_action)
    button.pack(pady=15)

    login.mainloop()