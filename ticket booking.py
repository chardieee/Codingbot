import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def setup_database():
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            ticket_id TEXT PRIMARY KEY,
            movie_name TEXT,
            available_tickets INTEGER,
            ticket_price INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)

    movies = [
        ("T1", "MOANA 2", 9, 300),
        ("T2", "UN/HAPPY FOR YOU", 4, 370),
        ("T3", "And The Bread Winner Is", 5, 400),
        ("T4", "Y2K", 2, 250),
        ("T5", "The Flash", 6, 250),
    ]

    cursor.execute("DELETE FROM movies")
    cursor.executemany("INSERT INTO movies VALUES (?, ?, ?, ?)", movies)
    conn.commit()
    conn.close()

def register_user():
    username = reg_username_entry.get().strip()
    password = reg_password_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Username already exists.")
        conn.close()
        return

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Account created successfully!")
    reg_username_entry.delete(0, tk.END)
    reg_password_entry.delete(0, tk.END)

def login_user():
    username = login_username_entry.get().strip()
    password = login_password_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()
    conn.close()

    if record and record[0] == password:
        messagebox.showinfo("Success", f"Welcome, {username}!")
        login_frame.pack_forget()
        main_app_frame.pack(fill="both", expand=True)
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# GUI Setup
root = tk.Tk()
root.title("Movie Ticket Booking System")
root.geometry("800x600")
root.configure(bg="black")

# Login Frame
login_frame = tk.Frame(root, bg="black")
login_frame.pack(fill="both", expand=True)

login_title = tk.Label(login_frame, text="Ticket Booking", font=("Comic Sans MS", 27, "bold"), bg="black", fg="magenta")
login_title.pack(pady=20)

login_username_label = tk.Label(login_frame, text="Username:", font=("Arial", 13), bg="black", fg="magenta")
login_username_label.pack(pady=5)
login_username_entry = tk.Entry(login_frame, font=("Arial", 12), width=25)
login_username_entry.pack(pady=5)

login_password_label = tk.Label(login_frame, text="Password:", font=("Arial", 13), bg="black", fg="magenta")
login_password_label.pack(pady=5)
login_password_entry = tk.Entry(login_frame, font=("Arial", 12), show="*", width=25)
login_password_entry.pack(pady=5)

login_button = tk.Button(login_frame, text="Login", font=("Arial", 12, "bold"), bg="blue", fg="white", command=login_user)
login_button.pack(pady=10)

register_button = tk.Button(login_frame, text="Register", font=("Arial", 12, "bold"), bg="blue", fg="white", command=lambda: show_register_frame())
register_button.pack(pady=10)

register_frame = tk.Frame(root, bg="black")

reg_title = tk.Label(register_frame, text="Register", font=("Comic Sans MS", 25, "bold"), bg="black", fg="magenta")
reg_title.pack(pady=20)

reg_username_label = tk.Label(register_frame, text="Username:", font=("Arial", 12), bg="black", fg="magenta")
reg_username_label.pack(pady=5)
reg_username_entry = tk.Entry(register_frame, font=("Arial", 12), width=25)
reg_username_entry.pack(pady=5)

reg_password_label = tk.Label(register_frame, text="Password:", font=("Arial", 12), bg="black", fg="magenta")
reg_password_label.pack(pady=5)
reg_password_entry = tk.Entry(register_frame, font=("Arial", 12), show="*", width=25)
reg_password_entry.pack(pady=5)

create_account_button = tk.Button(register_frame, text="Create Account", font=("Arial", 12, "bold"), bg="blue", fg="white", command=register_user)
create_account_button.pack(pady=10)

back_to_login_button = tk.Button(register_frame, text="Back to Login", font=("Arial", 12, "bold"), bg="blue", fg="white", command=lambda: show_login_frame())
back_to_login_button.pack(pady=10)

main_app_frame = tk.Frame(root, bg="black")

title_label = tk.Label(main_app_frame, text="Available Movie", font=("Comic Sans MS", 25, "bold"), bg="black", fg="magenta")
title_label.pack(pady=10)

style = ttk.Style()
style.theme_use("default")
style.configure(
    "Treeview",
    background="white",
    foreground="black",
    rowheight=25,
    fieldbackground="white",
    borderwidth=1
)
style.configure(
    "Treeview.Heading",
    background="blue",
    foreground="white",
    font=("Arial", 12, "bold"),
)
style.map("Treeview.Heading", background=[("active", "darkblue")])

columns = ("ticket_id", "movie_name", "available_tickets", "ticket_price")
movie_table = ttk.Treeview(main_app_frame, columns=columns, show="headings", height=8)

movie_table.heading("ticket_id", text="Ticket ID")
movie_table.heading("movie_name", text="Movie Name")
movie_table.heading("available_tickets", text="Available Tickets")
movie_table.heading("ticket_price", text="Ticket Price")

movie_table.column("ticket_id", width=100, anchor="center")
movie_table.column("movie_name", width=250, anchor="center")
movie_table.column("available_tickets", width=150, anchor="center")
movie_table.column("ticket_price", width=120, anchor="center")

movie_table.pack(pady=10)

def populate_table():
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()   
    cursor.execute("SELECT * FROM movies")
    rows = cursor.fetchall()
    conn.close()

    for row in movie_table.get_children():
        movie_table.delete(row)

    for movie in rows:
        movie_table.insert("", "end", values=movie)

def book_tickets():
    customer_name = customer_name_entry.get().strip()
    ticket_count = ticket_count_entry.get().strip()

    # Ensure valid input
    if not customer_name:
        messagebox.showerror("Error", "Please enter your name.")
        return
    if not ticket_count.isdigit() or int(ticket_count) <= 0:
        messagebox.showerror("Error", "Please enter a valid number of tickets.")
        return

    selected_item = movie_table.focus()  
    if not selected_item:
        messagebox.showerror("Error", "Please select a movie to book tickets for.")
        return

    selected_movie = movie_table.item(selected_item)["values"]
    ticket_id, movie_name, available_tickets, ticket_price = selected_movie

    if int(ticket_count) > available_tickets:
        messagebox.showerror("Error", "Not enough tickets available.")
        return

    total_price = int(ticket_count) * ticket_price

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE movies SET available_tickets = available_tickets - ? WHERE ticket_id = ?",
        (int(ticket_count), ticket_id),
    )
    conn.commit()
    conn.close()


    populate_table()

    with open("ticket_bookings.txt", "a") as file:
        file.write(
            f"=================================\n"
            f"Customer Name: {customer_name}  \n"
            f"Movie Name: {movie_name}\n"
            f"Tickets Booked: {ticket_count}\n"
            f"Total Price: P{total_price}\n"
            f"=================================\n"
        )

    messagebox.showinfo(
        "Success",
        f"Booking successful!\n\nCustomer Name: {customer_name}\nMovie: {movie_name}\nTickets: {ticket_count}\nTotal Price: ₱{total_price}",
    )

    customer_name_entry.delete(0, tk.END)
    ticket_count_entry.set("1")


populate_table()

details_frame = tk.Frame(main_app_frame, bg="black")
details_frame.pack(pady=10)

tk.Label(details_frame, text="Customer Name:", font=("Arial", 12), bg="black", fg="magenta").grid(row=0, column=0, padx=10, pady=5)
customer_name_entry = tk.Entry(details_frame, font=("Arial", 12), width=25)
customer_name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(details_frame, text="No. of Tickets:", font=("Arial", 12), bg="black", fg="magenta").grid(row=1, column=0, padx=10, pady=5)
ticket_count_entry = ttk.Combobox(details_frame, values=[str(i) for i in range(1, 11)], font=("Arial", 12), width=23)
ticket_count_entry.grid(row=1, column=1, padx=10, pady=5)
ticket_count_entry.set("")

book_button = tk.Button(main_app_frame, text="Book Tickets", font=("Arial", 12, "bold"), bg="magenta", fg="black")
book_button.pack(pady=10)

book_button.config(command=book_tickets)

populate_table()

# Update Movie Functionality
def update_movie():
    selected_item = movie_table.focus()
    if not selected_item:
        messagebox.showerror("Error", "Please select a movie to update.")
        return

    selected_movie = movie_table.item(selected_item)["values"]
    ticket_id = selected_movie[0]
    new_name = movie_name_entry.get().strip()
    new_price = ticket_price_entry.get().strip()

    if not new_name or not new_price.isdigit():
        messagebox.showerror("Error", "Please enter valid name and price.")
        return

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE movies SET movie_name = ?, ticket_price = ? WHERE ticket_id = ?", (new_name, int(new_price), ticket_id))
    conn.commit()
    conn.close()

    populate_table()

    movie_name_entry.delete(0, tk.END)
    ticket_price_entry.delete(0, tk.END)
    messagebox.showinfo("Success", f"Movie '{ticket_id}' updated successfully!")

# Input Fields for Update
update_frame = tk.Frame(main_app_frame, bg="black")
update_frame.pack(pady=10)

tk.Label(update_frame, text="New Movie Name:", font=("Arial", 12), bg="black", fg="magenta").grid(row=0, column=0, padx=10, pady=5)
movie_name_entry = tk.Entry(update_frame, font=("Arial", 12), width=25)
movie_name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(update_frame, text="New Ticket Price:", font=("Arial", 12), bg="black", fg="magenta").grid(row=1, column=0, padx=10, pady=5)
ticket_price_entry = tk.Entry(update_frame, font=("Arial", 12), width=25)
ticket_price_entry.grid(row=1, column=1, padx=10, pady=5)

update_button = tk.Button(main_app_frame, text="Update Movie", font=("Arial", 12, "bold"), bg="magenta", fg="black", command=update_movie)
update_button.pack(pady=10)



def show_register_frame():
    login_frame.pack_forget()
    register_frame.pack(fill="both", expand=True)

def show_login_frame():
    register_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

setup_database()
show_login_frame()

root.mainloop()





