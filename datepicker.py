from datetime import datetime, timedelta
import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import messagebox

date_range = {"start": None, "end": None}

def pick_date(root):
    btn_x = root.date_button.winfo_rootx()
    btn_y = root.date_button.winfo_rooty()
    top = ctk.CTkToplevel(root)
    top.title("Sélectionnez une date ou une période")
    top.geometry(f"+{btn_x}+{btn_y + root.date_button.winfo_height() + 5}")
    top.transient(root)
    top.update()
    top.grab_set()

    cal_frame = ctk.CTkFrame(top, corner_radius=12, fg_color="#2e2e2e")
    cal_frame.pack(padx=10, pady=10)

    today = datetime.today().date()
    cal = Calendar(cal_frame, selectmode="day", year=today.year, month=today.month, day=today.day,
                   background="#2e2e2e", foreground="white", selectbackground="#1f6aa5",
                   selectforeground="white", weekendbackground="#3a3a3a", weekendforeground="#7ec0ee",
                   othermonthforeground="#888888", bordercolor="#444444", headersbackground="#444444",
                   headersforeground="white", font=("Verdana", 12), maxdate=today)
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
            root.date_label.configure(text=f"Du {date_range['start'].strftime('%d/%m/%Y')} au {date_range['end'].strftime('%d/%m/%Y')}")
        elif date_range["start"]:
            root.date_label.configure(text=f"{date_range['start'].strftime('%d/%m/%Y')}")
        else:
            root.date_label.configure(text="Aucune date sélectionnée")

    cal.bind("<<CalendarSelected>>", on_click)

    ctk.CTkButton(top, text="OK", command=top.destroy,
                   corner_radius=12, fg_color="#1f6aa5", hover_color="#144870",
                   font=("Verdana", 14, "bold")).pack(pady=10)
