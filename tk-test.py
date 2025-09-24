import requests
import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime, timedelta
from tkinter import messagebox

# Mode nuit et thème
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

articles_links = {}
checkboxes = []
date_range = {"start": None, "end": None}

def fetch_articles():
    if not date_range["start"]:
        messagebox.showerror("Erreur", "Veuillez sélectionner au moins une date.")
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

    for widget in article_frame.winfo_children():
        widget.destroy()
    checkboxes.clear()
    articles_links.clear()

    toggle_btn = ctk.CTkButton(
        article_frame,
        text="Tout sélectionner",
        command=toggle_all,
        corner_radius=12,
        width=200
    )
    toggle_btn.pack(pady=5)
    article_frame.toggle_btn = toggle_btn

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
                    cb = ctk.CTkCheckBox(
                        article_frame,
                        text=f"{idx+1}. {title}",
                        variable=var,
                        font=("TakaoPGothic", 16),
                        corner_radius=8,
                        fg_color="#1f6aa5",
                        hover_color="#144870",
                        onvalue=True,
                        offvalue=False
                    )
                    cb.var = var
                    cb.pack(anchor="w", pady=3)
                    checkboxes.append((cb, idx))
                    idx += 1
                found = True
                break
        current_date += timedelta(days=1)

    if not found:
        ctk.CTkLabel(article_frame, text="Aucun article trouvé pour cette période").pack(anchor="w", pady=5)

def toggle_all():
    if not checkboxes:
        return
    all_selected = all(cb.var.get() for cb, _ in checkboxes)
    if all_selected:
        for cb, _ in checkboxes:
            cb.var.set(False)
        article_frame.toggle_btn.configure(text="Tout sélectionner")
    else:
        for cb, _ in checkboxes:
            cb.var.set(True)
        article_frame.toggle_btn.configure(text="Tout désélectionner")

def pick_date():
    # Positionner à côté du bouton
    btn_x = date_button.winfo_rootx()
    btn_y = date_button.winfo_rooty()
    top = ctk.CTkToplevel(root)
    top.title("Sélectionnez une date ou une période")
    top.geometry(f"+{btn_x}+{btn_y + date_button.winfo_height() + 5}")

    cal = Calendar(top, selectmode="day", year=2025, month=9, day=24)
    cal.pack(padx=10, pady=10)

    info_label = ctk.CTkLabel(top, text="Cliquez pour début/fin de période, recliquez sur la même date pour valider un jour seul.")
    info_label.pack(pady=5)

    last_click = {"date": None}
    selecting_period = {"in_progress": False}

    def clear_highlight():
        cal.calevent_remove("all")  # supprime tous les calevents et réinitialise les couleurs

    def highlight_range(start, end):
        clear_highlight()
        if start == end:
            cal.calevent_create(start, "start", "start")
        else:
            cal.calevent_create(start, "start", "start")
            cal.calevent_create(end, "end", "end")
            cur = start + timedelta(days=1)
            while cur < end:
                cal.calevent_create(cur, "highlight", "highlight")
                cur += timedelta(days=1)
        cal.tag_config('highlight', background="#4da6ff", foreground="black")
        cal.tag_config('start', background="#0066cc", foreground="white")
        cal.tag_config('end', background="#3399ff", foreground="white")

    def update_date_label():
        if date_range["start"] and date_range["end"] and date_range["start"] != date_range["end"]:
            date_label.configure(
                text=f"Du {date_range['start'].strftime('%d/%m/%Y')} au {date_range['end'].strftime('%d/%m/%Y')}"
            )
        elif date_range["start"]:
            date_label.configure(
                text=f"{date_range['start'].strftime('%d/%m/%Y')}"
            )
        else:
            date_label.configure(text="Aucune date sélectionnée")

    def on_click(event):
        selected = cal.selection_get()

        # Reset highlight si on commence une nouvelle période
        if not selecting_period["in_progress"]:
            clear_highlight()
            date_range["start"] = selected
            date_range["end"] = selected
            selecting_period["in_progress"] = True
        else:
            # Deuxième clic = fin de période
            if selected < date_range["start"]:
                date_range["end"], date_range["start"] = date_range["start"], selected
            else:
                date_range["end"] = selected
            highlight_range(date_range["start"], date_range["end"])
            selecting_period["in_progress"] = False

        # Re-clic sur la même date = journée unique
        if last_click["date"] == selected and date_range["start"] == date_range["end"] == selected:
            top.after(1, top.destroy)  # <-- remplace top.destroy() direct


        last_click["date"] = selected
        update_date_label()

    cal.bind("<<CalendarSelected>>", on_click)
    ctk.CTkButton(top, text="OK", command=top.destroy, corner_radius=12).pack(pady=5)

def suivant():
    selected_articles = []
    selected_links = []
    for cb, idx in checkboxes:
        if cb.var.get():
            selected_articles.append(cb.cget("text"))
            selected_links.append(articles_links[idx])

    if not selected_articles:
        messagebox.showinfo("Aucun article sélectionné", "Veuillez cocher au moins un article.")
        return

    msg = "\n".join(f"{title} -> {link}" for title, link in zip(selected_articles, selected_links))
    messagebox.showinfo("Articles sélectionnés", msg)

# Fenêtre principale
root = ctk.CTk()
root.title("NHK Easy Articles")
root.geometry("900x550")
root.resizable(False, False)

# Zone liste des articles avec scroll
article_frame = ctk.CTkScrollableFrame(root, width=850, height=300)
article_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Zone des dates
date_frame = ctk.CTkFrame(root)
date_frame.pack(pady=10, fill="x")

date_button = ctk.CTkButton(date_frame, text="Choisir une date/période", command=pick_date, corner_radius=12)
date_button.pack(side="left", padx=5)

date_label = ctk.CTkLabel(date_frame, text="Aucune date sélectionnée", font=("TakaoPGothic", 14))
date_label.pack(side="left", padx=10)

# Boutons en bas
button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=15)

ctk.CTkButton(button_frame, text="Rechercher", command=fetch_articles, corner_radius=12, width=150).pack(side="left", padx=20)
ctk.CTkButton(button_frame, text="Suivant", command=suivant, corner_radius=12, width=150).pack(side="left", padx=20)

root.mainloop()
