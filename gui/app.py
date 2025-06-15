import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

root = tk.Tk()
root.title("Library GUI")
root.geometry("600x600")

API_URL = "http://127.0.0.1:5000"

def update_list():
    listbox.delete(0, tk.END)
    try:
        response = requests.get(f"{API_URL}/books")
        for book in response.json():
            listbox.insert(tk.END, f"{book['title']} by {book['author']} (ISBN: {book['isbn']})")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()
    size = size_entry.get()
    is_ebook = ebook_var.get()

    if not title or not author or not isbn:
        messagebox.showerror("Error", "Title, Author, and ISBN required.")
        return

    data = {
        'title': title,
        'author': author,
        'isbn': isbn,
        'is_ebook': is_ebook,
        'size': size if is_ebook else None
    }

    try:
        response = requests.post(f"{API_URL}/books", json=data)
        update_list()
        messagebox.showinfo("Success", "Book added.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def remove_book():
    isbn = simpledialog.askstring("Remove", "Enter ISBN:")
    requests.delete(f"{API_URL}/books/{isbn}")
    update_list()

def lend_book():
    isbn = simpledialog.askstring("Lend", "Enter ISBN:")
    requests.post(f"{API_URL}/lend/{isbn}")
    update_list()

def return_book():
    isbn = simpledialog.askstring("Return", "Enter ISBN:")
    requests.post(f"{API_URL}/return/{isbn}")
    update_list()

def view_book():
    isbn = simpledialog.askstring("View Book", "Enter ISBN:")
    response = requests.get(f"{API_URL}/books/{isbn}")
    if response.status_code == 200:
        book = response.json()
        messagebox.showinfo("Book", f"Title: {book['title']}\nAuthor: {book['author']}\nAvailable: {book['available']}")
    else:
        messagebox.showerror("Not Found", "Book not found.")

def update_book():
    isbn = simpledialog.askstring("Update Book", "Enter ISBN:")
    new_title = simpledialog.askstring("New Title", "Leave blank to keep same")
    new_author = simpledialog.askstring("New Author", "Leave blank to keep same")

    data = {}
    if new_title:
        data['title'] = new_title
    if new_author:
        data['author'] = new_author

    response = requests.put(f"{API_URL}/books/{isbn}", json=data)
    update_list()
    if response.status_code == 200:
        messagebox.showinfo("Updated", "Book updated.")
    else:
        messagebox.showerror("Error", "Book not found.")

# Widgets
tk.Label(root, text="Title").pack()
title_entry = tk.Entry(root)
title_entry.pack()

tk.Label(root, text="Author").pack()
author_entry = tk.Entry(root)
author_entry.pack()

tk.Label(root, text="ISBN").pack()
isbn_entry = tk.Entry(root)
isbn_entry.pack()

ebook_var = tk.BooleanVar()
tk.Checkbutton(root, text="eBook?", variable=ebook_var).pack()

tk.Label(root, text="Download Size (MB)").pack()
size_entry = tk.Entry(root)
size_entry.pack()

tk.Button(root, text="Add Book", command=add_book).pack(pady=2)
tk.Button(root, text="Remove Book", command=remove_book).pack(pady=2)
tk.Button(root, text="Lend Book", command=lend_book).pack(pady=2)
tk.Button(root, text="Return Book", command=return_book).pack(pady=2)
tk.Button(root, text="View Book", command=view_book).pack(pady=2)
tk.Button(root, text="Update Book", command=update_book).pack(pady=2)

listbox = tk.Listbox(root, width=70)
listbox.pack(pady=10)

update_list()
root.mainloop()
