import tkinter as tk
from tkinter import ttk
from services.rental_service import load_rentals


class RentalHistoryWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Kiralama Geçmişi")
        self.window.geometry("800x400")

        columns = (
            "plaka",
            "musteri",
            "baslangic",
            "bitis",
            "gun_sayisi",
            "gunluk_ucret",
            "toplam_ucret",
            "created_at"
        )

        self.tree = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings"
        )

        headings = {
            "plaka": "Plaka",
            "musteri": "Müşteri",
            "baslangic": "Başlangıç",
            "bitis": "Bitiş",
            "gun_sayisi": "Gün",
            "gunluk_ucret": "Günlük Ücret",
            "toplam_ucret": "Toplam Ücret",
            "created_at": "Kayıt Zamanı"
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_history()

    def load_history(self):
        self.tree.delete(*self.tree.get_children())

        for r in load_rentals():
            self.tree.insert(
                "",
                tk.END,
                values=(
                    r["plaka"],
                    r["musteri"],
                    r["baslangic"],
                    r["bitis"],
                    r["gun_sayisi"],
                    f'{r["gunluk_ucret"]} ₺',
                    f'{r["toplam_ucret"]} ₺',
                    r["created_at"]
                )
            )
