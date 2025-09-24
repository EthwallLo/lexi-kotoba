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

# --- Fonctions ---
def fetch_articles():
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

    # Reset de la zone articles
    for widget in article_frame.winfo_children():
        widget.destroy()
    checkboxes.clear()
    articles_links.clear()

    # Bouton Tout sélectionner / désélectionner
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
                        font=("Verdana", 16),
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
    for cb, _ in checkboxes:
        cb.var.set(not all_selected)
    article_frame.toggle_btn.configure(
        text="Tout désélectionner" if not all_selected else "Tout sélectionner"
    )

def pick_date():
    btn_x = date_button.winfo_rootx()
    btn_y = date_button.winfo_rooty()
    top = ctk.CTkToplevel(root)
    top.title("Sélectionnez une date ou une période")
    top.geometry(f"+{btn_x}+{btn_y + date_button.winfo_height() + 5}")
    top.transient(root)
    top.update()
    top.grab_set()

    cal_frame = ctk.CTkFrame(top, corner_radius=12, fg_color="#2e2e2e")
    cal_frame.pack(padx=10, pady=10)

    today = datetime.today().date()
    cal = Calendar(
        cal_frame,
        selectmode="day",
        year=today.year,
        month=today.month,
        day=today.day,
        background="#2e2e2e",
        foreground="white",
        selectbackground="#1f6aa5",
        selectforeground="white",
        weekendbackground="#3a3a3a",
        weekendforeground="#7ec0ee",
        othermonthforeground="#888888",
        bordercolor="#444444",
        headersbackground="#444444",
        headersforeground="white",
        font=("Verdana", 12),
        maxdate=today
    )
    cal.pack(padx=5, pady=5)

    info_label = ctk.CTkLabel(top, text="Cliquez pour début/fin de période. Validez avec OK.", font=("Verdana", 12))
    info_label.pack(pady=5)

    selecting_period = {"in_progress": False}

    def clear_highlight():
        cal.calevent_remove("all")

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

    def on_click(event):
        selected = cal.selection_get()
        if not selecting_period["in_progress"] or (date_range["start"] and date_range["end"]):
            clear_highlight()
            date_range["start"] = selected
            date_range["end"] = None
            selecting_period["in_progress"] = True
            highlight_range(date_range["start"], date_range["start"])
        else:
            if selected < date_range["start"]:
                date_range["end"], date_range["start"] = date_range["start"], selected
            else:
                date_range["end"] = selected
            highlight_range(date_range["start"], date_range["end"])
            selecting_period["in_progress"] = False

        if date_range["start"] and date_range["end"] and date_range["end"] != date_range["start"]:
            date_label.configure(text=f"Du {date_range['start'].strftime('%d/%m/%Y')} au {date_range['end'].strftime('%d/%m/%Y')}")
        elif date_range["start"]:
            date_label.configure(text=f"{date_range['start'].strftime('%d/%m/%Y')}")
        else:
            date_label.configure(text="Aucune date sélectionnée")

    cal.bind("<<CalendarSelected>>", on_click)

    ctk.CTkButton(
        top,
        text="OK",
        command=top.destroy,
        corner_radius=12,
        fg_color="#1f6aa5",
        hover_color="#144870",
        font=("Verdana", 14, "bold")
    ).pack(pady=10)

# --- Navigation ---
def suivant():
    selected_articles = [cb.cget("text") for cb, idx in checkboxes if cb.var.get()]
    if not selected_articles:
        messagebox.showinfo("Aucun article sélectionné", "Veuillez cocher au moins un article.")
        return

    page2_text.configure(state="normal")
    page2_text.delete("0.0", "end")
    for title in selected_articles:
        page2_text.insert("end", f"{title}\n")
    page2_text.configure(state="disabled")

    # Cacher page 1 (articles + boutons + date)
    article_frame.pack_forget()
    button_frame.pack_forget()
    date_frame.pack_forget()
    page2_frame.pack(fill="both", expand=True)

def precedent():
    page2_frame.pack_forget()
    article_frame.pack(padx=10, pady=10, fill="both", expand=True)
    button_frame.pack(pady=15)
    date_frame.pack(pady=10, fill="x")

def recuperer_vocabulaire():
    pass  # pour l'instant ne fait rien

# --- Fenêtre principale ---
root = ctk.CTk()
root.title("NHK Easy Articles")
root.geometry("900x550")
root.resizable(False, False)

# Page 1
article_frame = ctk.CTkScrollableFrame(root, width=850, height=300)
article_frame.pack(padx=10, pady=10, fill="both", expand=True)

date_frame = ctk.CTkFrame(root)
date_frame.pack(pady=10, fill="x")
date_button = ctk.CTkButton(date_frame, text="Choisir une date/période", command=pick_date, corner_radius=12)
date_button.pack(side="left", padx=5)
date_label = ctk.CTkLabel(date_frame, text="Aucune date sélectionnée", font=("Verdana", 14))
date_label.pack(side="left", padx=10)

button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=15)
ctk.CTkButton(button_frame, text="Rechercher", command=fetch_articles, corner_radius=12,
               fg_color="#1f6aa5", hover_color="#144870", font=("Verdana", 14)).pack(side="left", padx=5)
ctk.CTkButton(button_frame, text="Suivant", command=suivant, corner_radius=12,
               fg_color="#1f6aa5", hover_color="#144870", font=("Verdana", 14)).pack(side="left", padx=5)

# Page 2
page2_frame = ctk.CTkFrame(root)
page2_text = ctk.CTkTextbox(page2_frame, width=780, height=400, font=("Verdana", 14))
page2_text.pack(padx=10, pady=10, fill="both", expand=True)
page2_text.configure(state="disabled")

button_frame2 = ctk.CTkFrame(page2_frame)
button_frame2.pack(pady=10)
ctk.CTkButton(button_frame2, text="Précédent", command=precedent, corner_radius=12,
               fg_color="#1f6aa5", hover_color="#144870", font=("Verdana", 14)).pack(side="left", padx=5)
ctk.CTkButton(button_frame2, text="Récupérer le vocabulaire", command=recuperer_vocabulaire,
               corner_radius=12, fg_color="#1f6aa5", hover_color="#144870", font=("Verdana", 14)).pack(side="left", padx=5)

root.mainloop()
