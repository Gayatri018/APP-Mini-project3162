#!/usr/bin/env python
# coding: utf-8

# In[1]:


#######################################################################################################3
#UPDATED CODE --LATEST
import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

def create_table():
    connection = sqlite3.connect("user_credentials.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR, password VARCHAR)")
    cursor.execute("CREATE TABLE IF NOT EXISTS bookings (username VARCHAR, movie_title VARCHAR)")
    connection.commit()
    connection.close()

def create_account(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    connection = sqlite3.connect("user_credentials.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    connection.commit()
    connection.close()
    messagebox.showinfo("Success", "Account created successfully!")

def login():
    global logged_in_user
    username = username_login.get()
    password = password_login.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    connection = sqlite3.connect("user_credentials.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    connection.close()

    if user:
        logged_in_user = username
        messagebox.showinfo("Success", "Login successful!")
        show_main_page()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def show_main_page():
    login_frame.pack_forget()
    main_page_frame.pack(padx=10, pady=10)

def show_confirmation_page(movie_title):
    main_page_frame.pack_forget()
    confirmation_frame.pack(padx=10, pady=10)
    tk.Label(confirmation_frame, text=f"Selected Movie: {movie_title}").pack(pady=10)
    tk.Button(confirmation_frame, text="Yes, Confirm My Booking", command=lambda title=movie_title: confirm_booking(title)).pack(pady=10)
    tk.Button(confirmation_frame, text="Return to Main Page", command=return_to_main_page).pack(pady=10)
    exit_button = tk.Button(confirmation_frame, text="Exit", command=root.destroy, bg="red", fg="white").pack(padx=10)

def confirm_booking(movie_title):
    global logged_in_user
    connection = sqlite3.connect("user_credentials.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bookings WHERE username=?", (logged_in_user,))
    existing_booking = cursor.fetchone()
    cursor.execute("INSERT INTO bookings VALUES (?, ?)", (logged_in_user, movie_title))
    connection.commit()
    connection.close()
    messagebox.showinfo("Success", f"Booking confirmed for {logged_in_user} for {movie_title}!")

def return_to_main_page():
    confirmation_frame.pack_forget()
    main_page_frame.pack(padx=10, pady=10)

root = tk.Tk()
root.title("Movie Booking System")
create_table()

# account creation (also page1 link given to this page)
def create_acc():
    global create_acc_frame 
    login_frame.pack_forget()
    
    create_acc_frame = tk.Frame(root)
    create_acc_frame.pack()
    
    create_acc_frame.pack(padx=10, pady=10)
    tk.Label(create_acc_frame, text="Create Account").pack(pady=10)

    tk.Label(create_acc_frame, text="Username:").pack()
    global username_entry 
    username_entry = tk.Entry(create_acc_frame)
    username_entry.pack(pady=10)

    tk.Label(create_acc_frame, text="Password:").pack()
    global password_entry 
    password_entry = tk.Entry(create_acc_frame)
    password_entry.pack(pady=10)

    create_acc_button = tk.Button(create_acc_frame, text="Create Account", command=lambda: create_account(username_entry, password_entry))
    create_acc_button.pack(pady=10)

    
    
    def create_account(username_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        connection = sqlite3.connect("user_credentials.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Account created successfully!")
        create_acc_frame.pack_forget()
        login_frame.pack(padx=10, pady=10)
        
        
      
        

# login page(page 1)
login_frame = tk.Frame(root)
login_frame.pack(padx=10, pady=10)
tk.Label(login_frame, text="Login").pack(pady=10)

tk.Label(login_frame, text="Username:").pack()
username_login = tk.Entry(login_frame)
username_login.pack(pady=10)

tk.Label(login_frame, text="Password:").pack()
password_login = tk.Entry(login_frame)
password_login.pack(pady=10)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.pack(pady=10)

create_acc_btn = tk.Button(login_frame, text="Create Account", command=create_acc).pack(padx=10, pady=10)

# main page for movie booking(page 2 for my project)
main_page_frame = tk.Frame(root)


# movie images and titles with prices
movie_data = [
    {"image_path": "C:/Users/HP/Downloads/movie1.png", "title": "Spiderman\n₹499\nper person"},
    {"image_path": "C:/Users/HP/Downloads/movie2.png", "title": "Avengers\n₹399\nper person"},
    {"image_path": "C:/Users/HP/Downloads/movie3.png", "title": "War\n₹299\n"},
    {"image_path": "C:/Users/HP/Downloads/movie4.png", "title": "Scary Movie\n₹499\nper person"}
]

#images used in the page3
movie_images = []

def select_movie(movie_title):
    show_confirmation_page(movie_title)

for movie in movie_data:
    movie_image_path = movie["image_path"]
    movie_title = movie["title"]

    original_image = Image.open(movie_image_path)
    resized_image = original_image.resize((150, 150), Image.LANCZOS)
    movie_image = ImageTk.PhotoImage(resized_image)
    movie_images.append(movie_image)  # Store the PhotoImage in the list

    label_movie = tk.Label(main_page_frame, image=movie_image)
    label_movie.image = movie_image  # Keep a reference to the image
    label_movie.pack(side=tk.LEFT, padx=10, pady=10)

    tk.Radiobutton(main_page_frame, text=f"Select {movie_title}", variable=tk.StringVar(), value=movie_title,
                   command=lambda title=movie_title: select_movie(title)).pack(side=tk.LEFT, pady=10)


# page 3 -- this will come after i click on any movie on page 2
confirmation_frame = tk.Frame(root)

root.mainloop()


# In[ ]:




