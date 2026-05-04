import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "data/movies.json"

def load_movies():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_movies(movies):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

def add_movie():
    title = entry_title.get().strip()
    genre = entry_genre.get().strip()
    year = entry_year.get().strip()
    rating = entry_rating.get().strip()

    if not title or not genre or not year or not rating:
        messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
        return

    if not year.isdigit() or int(year) < 1895 or int(year) > 2026:
        messagebox.showerror("Ошибка", "Год должен быть числом от 1895 до 2026!")
        return

    if not (rating.replace('.', '', 1).isdigit() and 0 <= float(rating) <= 10):
        messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10!")
        return

    movie = {"title": title, "genre": genre, "year": int(year), "rating": float(rating)}
    movies.append(movie)
    save_movies(movies)
    update_table()
    clear_entries()

def clear_entries():
    entry_title.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)

def update_table(filter_genre=None, filter_year=None):
    for i in tree.get_children():
        tree.delete(i)
    for movie in movies:
        if filter_genre and movie["genre"].lower() != filter_genre.lower():
            continue
        if filter_year and str(movie["year"]) != filter_year:
            continue
        tree.insert("", tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

def on_filter():
    genre = combo_genre.get()
    year = combo_year.get()
    update_table(genre if genre != "Все" else None, year if year != "Все" else None)

# --- Основное окно ---
root = tk.Tk()
root.title("Movie Library")
root.geometry("800x500")

movies = load_movies()

# --- Поля ввода ---
tk.Label(root, text="Название:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_title = tk.Entry(root, width=30)
entry_title.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Жанр:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_genre = tk.Entry(root, width=30)
entry_genre.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Год:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_year = tk.Entry(root, width=10)
entry_year.grid(row=2, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Рейтинг:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_rating = tk.Entry(root, width=10)
entry_rating.grid(row=3, column=1, padx=10, pady=5, sticky="w")

btn_add = tk.Button(root, text="Добавить фильм", command=add_movie)
btn_add.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# --- Фильтрация ---
tk.Label(root, text="Фильтр по жанру:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
genres = sorted({m["genre"] for m in movies} | {"Все"})
combo_genre = ttk.Combobox(root, values=genres, state="readonly")
combo_genre.current(0)
combo_genre.grid(row=5, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Фильтр по году:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
years = sorted({str(m["year"]) for m in movies} | {"Все"})
combo_year = ttk.Combobox(root, values=years, state="readonly")
combo_year.current(0)
combo_year.grid(row=6, column=1, padx=10, pady=5, sticky="w")

btn_filter = tk.Button(root, text="Применить фильтр", command=on_filter)
btn_filter.grid(row=7, column=1, padx=10, pady=10, sticky="w")

# --- Таблица ---
columns = ("Название", "Жанр", "Год", "Рейтинг")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180)
tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

update_table()

root.mainloop()