import requests
import customtkinter as ctk
from datetime import timedelta
from datepicker import date_range
from tkinter import messagebox

articles_links = {}
checkboxes = []

def fetch_articles(root):
    if not date_range["start"]:
        messagebox.showerror("Erreur", "Veuillez sélectionner au moins une date ou une période.")
        return

    start_api = date_range["start"]
    end_api = date_range["end"] if date_range["end"] else date_range["start"]

    url = "https://www3.nhk.or.jp/news/easy/news-list.json"
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de récupérer les articles : {e}")
        return

    # Reset
    for widget in root.article_frame.winfo_children():
        widget.destroy()
    checkboxes.clear()
    articles_links.clear()

    toggle_btn = ctk.CTkButton(root.article_frame, text="Tout sélectionner", command=lambda: toggle_all(root), corner_radius=12, width=200)
    toggle_btn.pack(pady=5)
    root.article_frame.toggle_btn = toggle_btn

    found = False
    idx = 0
    current_date = start_api

    while current_date <= end_api:
        date_api = current_date.strftime("%Y-%m-%d")
        for item in data:
            if date_api in item:
                articles = item[date_api]
                for article in articles:
                    title = article.get("title", "Pas de titre")
                    link = article.get("news_web_url", "")
                    articles_links[idx] = link

                    var = ctk.BooleanVar()
                    cb = ctk.CTkCheckBox(root.article_frame, text=f"{idx+1}. {title}", variable=var,
                                          font=("Verdana", 16), corner_radius=8, fg_color="#1f6aa5",
                                          hover_color="#144870", onvalue=True, offvalue=False)
                    cb.var = var
                    cb.pack(anchor="w", pady=3)
                    checkboxes.append((cb, idx))
                    idx += 1
                found = True
                break
        current_date += timedelta(days=1)

    if not found:
        ctk.CTkLabel(root.article_frame, text="Aucun article trouvé pour cette période").pack(anchor="w", pady=5)

def toggle_all(root):
    if not checkboxes:
        return
    all_selected = all(cb.var.get() for cb, _ in checkboxes)
    for cb, _ in checkboxes:
        cb.var.set(not all_selected)
    root.article_frame.toggle_btn.configure(text="Tout désélectionner" if not all_selected else "Tout sélectionner")
