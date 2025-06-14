import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

API_URL = "http://localhost:5000"

root = tk.Tk()
root.title("Library Management System")
root.geometry("600x600")

def toggle_ebook_field():
    if ebook_var.get():
        size_entry.config(state='normal')
    else:
        size_entry.delete(0, tk.END)
        size_entry.config(state='disabled')

def validate_size(P):
    return P == "" or P.isdigit()

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()
    size = size_entry.get()
    is_ebook = ebook_var.get()

    if not title or not author or not isbn:
        messagebox.showerror("Error", "All fields except size are required.")
        return

    data = {
        "title": title,
        "author": author,
        "isbn": isbn,
    }
    if is_ebook:
        if not size:
            messagebox.showerror("Error", "Size required for eBooks.")
            return
        data["download_size"] = float(size)

    try:
        r = requests.post(f"{API_URL}/books", json=data)
        if r.status_code == 201:
            messagebox.showinfo("Success", "Book added.")
            update_list()
        else:
            messagebox.showerror("Error", r.json().get("error", "Unknown error"))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def lend_book():
    isbn = simpledialog.askstring("Lend Book", "Enter ISBN:")
    if isbn:
        r = requests.put(f"{API_URL}/books/{isbn}/lend")
        if r.ok:
            update_list()
            messagebox.showinfo("Success", r.json()["message"])
        else:
            messagebox.showerror("Error", r.json().get("error", "Failed to lend."))

def return_book():
    isbn = simpledialog.askstring("Return Book", "Enter ISBN:")
    if isbn:
        r = requests.put(f"{API_URL}/books/{isbn}/return")
        if r.ok:
            update_list()
            messagebox.showinfo("Success", r.json()["message"])
        else:
            messagebox.showerror("Error", r.json().get("error", "Failed to return."))

def remove_book():
    isbn = simpledialog.askstring("Remove Book", "Enter ISBN:")
    if isbn:
        r = requests.delete(f"{API_URL}/books/{isbn}")
        if r.ok:
            update_list()
            messagebox.showinfo("Removed", r.json()["message"])

def search_by_author():
    author = simpledialog.askstring("Search", "Enter author:")
    if author:
        r = requests.get(f"{API_URL}/books/author/{author}")
        if r.ok:
            listbox.delete(0, tk.END)
            for book in r.json():
                listbox.insert(tk.END, f"{book['title']} by {book['author']} (ISBN: {book['isbn']})")

def update_list():
    r = requests.get(f"{API_URL}/books")
    if r.ok:
        listbox.delete(0, tk.END)
        for book in r.json():
            status = "Available" if book["available"] else "Lent"
            listbox.insert(tk.END, f"{book['title']} by {book['author']} (ISBN: {book['isbn']}) - {status}")

# GUI Widgets
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
tk.Checkbutton(root, text="eBook?", variable=ebook_var, command=toggle_ebook_field).pack()

tk.Label(root, text="Download Size (MB)").pack()
vcmd = (root.register(validate_size), '%P')
size_entry = tk.Entry(root, validate="key", validatecommand=vcmd)
size_entry.pack()
size_entry.config(state='disabled')

tk.Button(root, text="Add Book", command=add_book).pack(pady=5)
tk.Button(root, text="Lend Book", command=lend_book).pack(pady=5)
tk.Button(root, text="Return Book", command=return_book).pack(pady=5)
tk.Button(root, text="Remove Book", command=remove_book).pack(pady=5)
tk.Button(root, text="Search by Author", command=search_by_author).pack(pady=5)

listbox = tk.Listbox(root, width=70)
listbox.pack(pady=10)
update_list()

root.mainloop()
