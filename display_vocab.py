from articles import checkboxes
from tkinter import messagebox
from get_vocabulary import fetch_vocabulary 

def display_secondpage(root):
    selected_articles = [cb.cget("text") for cb, idx in checkboxes if cb.var.get()]
    if not selected_articles:
        messagebox.showinfo("No article selected", "Please select at least one article.")
        return

    root.page2_text.configure(state="normal")
    root.page2_text.delete("0.0", "end")
    for title in selected_articles:
        root.page2_text.insert("end", f"{title}\n")
    root.page2_text.configure(state="disabled")

    root.article_frame.pack_forget()
    root.date_frame.pack_forget()

    root.page2_frame.pack(fill="both", expand=True)

def previous(root):
    root.page2_frame.pack_forget()

    root.article_frame.pack(padx=10, pady=10, fill="both", expand=True)
    root.date_frame.pack(pady=10, fill="x")
