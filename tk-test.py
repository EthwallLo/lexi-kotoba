import requests
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta

# Dictionnaire pour garder en mémoire les liens des articles affichés
articles_links = {}

def fetch_articles():
    start_str = start_date.get()
    end_str = end_date.get()

    try:
        start_api = datetime.strptime(start_str, "%d/%m/%Y")
    except ValueError:
        article_listbox.delete(0, tk.END)
        article_listbox.insert(tk.END, "Date de début invalide ! Utilisez JJ/MM/AAAA")
        return

    if end_str.strip():
        try:
            end_api = datetime.strptime(end_str, "%d/%m/%Y")
        except ValueError:
            article_listbox.delete(0, tk.END)
            article_listbox.insert(tk.END, "Date de fin invalide ! Utilisez JJ/MM/AAAA")
            return
    else:
        end_api = start_api

    if end_api < start_api:
        article_listbox.delete(0, tk.END)
        article_listbox.insert(tk.END, "La date de fin doit être après la date de début")
        return

    url = "https://www3.nhk.or.jp/news/easy/news-list.json"
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        article_listbox.delete(0, tk.END)
        article_listbox.insert(tk.END, f"Erreur lors de la récupération des articles : {e}")
        return

    article_listbox.delete(0, tk.END)
    articles_links.clear()
    found = False

    # Parcours de toutes les dates entre start et end
    current_date = start_api
    while current_date <= end_api:
        date_api = current_date.strftime("%Y-%m-%d")
        for item in data:
            if date_api in item:
                articles = item[date_api]
                for i, article in enumerate(articles):
                    title = article.get('title', 'Pas de titre')
                    link = article.get('news_web_url', '')
                    # Affiche seulement le titre
                    article_listbox.insert(tk.END, title)
                    # Stocke le lien en mémoire
                    articles_links[article_listbox.size() - 1] = link
                found = True
                break
        current_date += timedelta(days=1)

    if not found:
        article_listbox.insert(tk.END, "Aucun article trouvé pour cette période")

def pick_date(target_var):
    def select():
        target_var.set(cal.selection_get().strftime("%d/%m/%Y"))
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Sélectionnez une date")
    cal = Calendar(top, selectmode='day', year=2025, month=9, day=24)
    cal.pack(padx=10, pady=10)
    tk.Button(top, text="OK", command=select).pack(pady=5)

def suivant():
    selected_indices = article_listbox.curselection()
    if not selected_indices:
        messagebox.showinfo("Aucun article sélectionné", "Veuillez sélectionner au moins un article.")
        return
    selected_articles = [article_listbox.get(i) for i in selected_indices]
    selected_links = [articles_links[i] for i in selected_indices]
    msg = "\n".join(f"{title} -> {link}" for title, link in zip(selected_articles, selected_links))
    messagebox.showinfo("Articles sélectionnés", msg)

# Création de la fenêtre principale
root = tk.Tk()
root.title("NHK Easy Articles")

# Listbox scrollable pour les résultats
frame_listbox = tk.Frame(root)
frame_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
article_listbox = tk.Listbox(frame_listbox, selectmode=tk.MULTIPLE, width=60, height=10, font=("TakaoPGothic", 18))
scrollbar = tk.Scrollbar(frame_listbox, orient=tk.VERTICAL, command=article_listbox.yview)
article_listbox.config(yscrollcommand=scrollbar.set)
article_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Zone en bas pour les dates et les boutons
bottom_frame = tk.Frame(root)
bottom_frame.pack(padx=10, pady=5, fill=tk.X)

tk.Label(bottom_frame, text="Date début (JJ/MM/AAAA) :").pack(side=tk.LEFT, padx=5)
start_date = tk.StringVar()
tk.Entry(bottom_frame, textvariable=start_date, width=12).pack(side=tk.LEFT, padx=5)
tk.Button(bottom_frame, text="Choisir", command=lambda: pick_date(start_date)).pack(side=tk.LEFT, padx=5)

tk.Label(bottom_frame, text="Date fin (optionnelle) :").pack(side=tk.LEFT, padx=5)
end_date = tk.StringVar()
tk.Entry(bottom_frame, textvariable=end_date, width=12).pack(side=tk.LEFT, padx=5)
tk.Button(bottom_frame, text="Choisir", command=lambda: pick_date(end_date)).pack(side=tk.LEFT, padx=5)

tk.Button(bottom_frame, text="Rechercher", command=fetch_articles).pack(side=tk.LEFT, padx=5)
tk.Button(bottom_frame, text="Suivant", command=suivant).pack(side=tk.RIGHT, padx=5)

root.mainloop()
