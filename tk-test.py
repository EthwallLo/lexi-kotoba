import requests
import tkinter as tk
from tkinter import scrolledtext

def fetch_articles():
    date = entry_date.get().strip()
    url = "https://www3.nhk.or.jp/news/easy/news-list.json"
    response = requests.get(url)
    data = response.json()
    
    # Effacer le texte précédent
    output_text.delete(1.0, tk.END)
    
    found = False
    for item in data:
        if date in item:
            articles = item[date]
            for i, article in enumerate(articles):
                output_text.insert(tk.END, f"{i}: {article.get('news_web_url')}\n")
            found = True
            break
            
    if not found:
        output_text.insert(tk.END, f"Aucun article trouvé pour la date {date}\n")

# Création de la fenêtre principale
root = tk.Tk()
root.title("NHK Easy Articles")

# Label et champ pour la date
tk.Label(root, text="Entrez une date (YYYY-MM-DD) :").pack(padx=10, pady=5)
entry_date = tk.Entry(root)
entry_date.pack(padx=10, pady=5)

# Bouton pour lancer la recherche
tk.Button(root, text="Rechercher", command=fetch_articles).pack(pady=5)

# Zone de texte pour afficher les résultats avec scroll
output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(padx=10, pady=10)

# Lancer la boucle principale
root.mainloop()
