import requests
import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime, timedelta
from tkinter import messagebox

# Mode nuit et thème
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

articles_links = {}
selected_indices = set()  # gestion de la sélection multiple

def fetch_articles():
    start_str = start_date.get()
    end_str = end_date.get()

    try:
        start_api = datetime.strptime(start_str, "%d/%m/%Y")
    except ValueError:
        article_box.configure(state="normal")
        article_box.delete("1.0", "end")
        article_box.insert("end", "Date de début invalide ! JJ/MM/AAAA\n")
        article_box.configure(state="disabled")
        return

    if end_str.strip():
        try:
            end_api = datetime.strptime(end_str, "%d/%m/%Y")
        except ValueError:
            article_box.configure(state="normal")
            article_box.delete("1.0", "end")
            article_box.insert("end", "Date de fin invalide ! JJ/MM/AAAA\n")
            article_box.configure(state="disabled")
            return
    else:
        end_api = start_api

    if end_api < start_api:
        article_box.configure(state="normal")
        article_box.delete("1.0", "end")
        article_box.insert("end", "La date de fin doit être après la date de début\n")
        article_box.configure(state="disabled")
        return

    url = "https://www3.nhk.or.jp/news/easy/news-list.json"
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        article_box.configure(state="normal")
        article_box.delete("1.0", "end")
        article_box.insert("end", f"Erreur récupération articles : {e}\n")
        article_box.configure(state="disabled")
        return

    # reset
    article_box.configure(state="normal")
    article_box.delete("1.0", "end")
    articles_links.clear()
    selected_indices.clear()
    found = False
    idx = 0

    current_date = start_api
    while current_date <= end_api:
        date_api = current_date.strftime("%Y-%m-%d")
        for item in data:
            if date_api in item:
                articles = item[date_api]
                for article in articles:
                    title = article.get('title', 'Pas de titre')
                    link = article.get('news_web_url', '')
                    articles_links[idx] = link
                    article_box.insert("end", f"{idx+1}. {title}\n")
                    idx += 1
                found = True
                break
        current_date += timedelta(days=1)

    if not found:
        article_box.insert("end", "Aucun article trouvé pour cette période\n")

    article_box.configure(state="disabled")

def pick_date(target_var):
    def select():
        target_var.set(cal.selection_get().strftime("%d/%m/%Y"))
        top.destroy()

    top = ctk.CTkToplevel(root)
    top.title("Sélectionnez une date")
    cal = Calendar(top, selectmode='day', year=2025, month=9, day=24)
    cal.pack(padx=10, pady=10)
    ctk.CTkButton(top, text="OK", command=select, corner_radius=12).pack(pady=5)

def toggle_select(event):
    """Permet de sélectionner/désélectionner un article en cliquant dessus"""
    index = int(float(event.y) // 30)  # hauteur approx ligne
    if index in articles_links:
        if index in selected_indices:
            selected_indices.remove(index)
        else:
            selected_indices.add(index)
        highlight_selection()

def highlight_selection():
    """Met en évidence les articles sélectionnés"""
    article_box.tag_remove("selected", "1.0", "end")
    for idx in selected_indices:
        start = f"{idx+1}.0"
        end = f"{idx+1}.end"
        article_box.tag_add("selected", start, end)
    article_box.tag_config("selected", background="#1f538d", foreground="white")

def suivant():
    if not selected_indices:
        messagebox.showinfo("Aucun article sélectionné", "Veuillez sélectionner au moins un article.")
        return
    selected_articles = []
    selected_links = []
    for idx in sorted(selected_indices):
        line = article_box.get(f"{idx+1}.0", f"{idx+1}.end").strip()
        selected_articles.append(line)
        selected_links.append(articles_links[idx])
    msg = "\n".join(f"{title} -> {link}" for title, link in zip(selected_articles, selected_links))
    messagebox.showinfo("Articles sélectionnés", msg)

# Fenêtre principale
root = ctk.CTk()
root.title("NHK Easy Articles")
root.geometry("900x550")
root.resizable(False, False)

# Zone liste des articles
article_box = ctk.CTkTextbox(root, width=850, height=350, font=("TakaoPGothic", 18))
article_box.pack(padx=10, pady=10, fill="both")
article_box.bind("<Button-1>", toggle_select)
article_box.configure(state="disabled")

# Zone des dates
date_frame = ctk.CTkFrame(root)
date_frame.pack(pady=10, fill="x")

ctk.CTkLabel(date_frame, text="Date début (JJ/MM/AAAA) :").pack(side="left", padx=5)
start_date = ctk.StringVar()
ctk.CTkEntry(date_frame, textvariable=start_date, width=120).pack(side="left", padx=5)
ctk.CTkButton(date_frame, text="Choisir", command=lambda: pick_date(start_date), corner_radius=12).pack(side="left", padx=5)

ctk.CTkLabel(date_frame, text="Date fin (optionnelle) :").pack(side="left", padx=15)
end_date = ctk.StringVar()
ctk.CTkEntry(date_frame, textvariable=end_date, width=120).pack(side="left", padx=5)
ctk.CTkButton(date_frame, text="Choisir", command=lambda: pick_date(end_date), corner_radius=12).pack(side="left", padx=5)

# Boutons en bas
button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=15)

ctk.CTkButton(button_frame, text="Rechercher", command=fetch_articles, corner_radius=12, width=150).pack(side="left", padx=20)
ctk.CTkButton(button_frame, text="Suivant", command=suivant, corner_radius=12, width=150).pack(side="left", padx=20)

root.mainloop()
