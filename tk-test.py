import requests
import tkinter as tk
from tkinter import scrolledtext
from tkcalendar import Calendar
from datetime import datetime

def fetch_articles():
    # Récupérer la date depuis le champ principal
    date_str = selected_date.get()
    try:
        date_api = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Format de date invalide ! Utilisez JJ/MM/AAAA\n")
        return

    url = "https://www3.nhk.or.jp/news/easy/news-list.json"
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Erreur lors de la récupération des articles : {e}\n")
        return

    output_text.delete(1.0, tk.END)
    found = False
    for item in data:
        if date_api in item:
            articles = item[date_api]
            for i, article in enumerate(articles):
                title = article.get('title', 'Pas de titre')
                link = article.get('news_web_url', 'Pas de lien')
                output_text.insert(tk.END, f"{i+1}: {title} -> {link}\n")
            found = True
            break
    if not found:
        output_text.insert(tk.END, f"Aucun article trouvé pour la date {date_str}\n")

def pick_date():
    def select():
        selected_date.set(cal.selection_get().strftime("%d/%m/%Y"))
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Sélectionnez une date")
    cal = Calendar(top, selectmode='day', year=2025, month=9, day=24)
    cal.pack(padx=10, pady=10)
    tk.Button(top, text="OK", command=select).pack(pady=5)

# Création de la fenêtre principale
root = tk.Tk()
root.title("NHK Easy Articles")

# Zone de texte scrollable pour les résultats
output_text = scrolledtext.ScrolledText(root, width=80, height=20, font=("TakaoPGothic", 12))
output_text.pack(padx=10, pady=10)

# Champ pour la date
selected_date = tk.StringVar()
tk.Label(root, text="Date sélectionnée (JJ/MM/AAAA) :").pack(padx=10, pady=2)
tk.Entry(root, textvariable=selected_date).pack(padx=10, pady=2)

# Boutons pour rechercher et ouvrir le calendrier
tk.Button(root, text="Rechercher", command=fetch_articles).pack(pady=5)
tk.Button(root, text="Choisir une date", command=pick_date).pack(pady=5)

root.mainloop()
