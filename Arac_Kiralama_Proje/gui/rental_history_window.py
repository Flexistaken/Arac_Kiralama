import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from services.rental_service import load_rentals


class RentalHistoryWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Kiralama Geçmişi ve Arşiv")
        self.geometry("1100x600")
        self.attributes("-topmost", True)

        # --- Stil Yapılandırması (Tabloyu Güzelleştirme) ---
        style = ttk.Style()
        style.configure("History.Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=35,
                        fieldbackground="#2a2d2e",
                        borderwidth=0,
                        font=("Roboto", 10))
        style.map('History.Treeview', background=[('selected', '#1f538d')])

        style.configure("History.Treeview.Heading",
                        background="#1f1f1f",
                        foreground="white",
                        relief="flat",
                        font=("Roboto", 11, "bold"))

        # Üst Başlık ve Bilgi Kartı
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1f538d")
        self.header_frame.pack(fill="x", pady=(0, 20))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="📜 Tüm Kiralama Kayıtları",
            font=("Roboto", 22, "bold"),
            text_color="white"
        )
        self.title_label.pack(pady=20)

        # Tablo Konteynırı (Frame)
        self.container = ctk.CTkFrame(self, corner_radius=15)
        self.container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Scrollbar (Kaydırma Çubuğu)
        self.scrollbar = ctk.CTkScrollbar(self.container)
        self.scrollbar.pack(side="right", fill="y", padx=2)

        # Treeview (Tablo)
        columns = (
            "plaka", "musteri", "baslangic", "bitis",
            "gun_sayisi", "gunluk_ucret", "toplam_ucret", "created_at"
        )

        self.tree = ttk.Treeview(
            self.container,
            columns=columns,
            show="headings",
            style="History.Treeview",
            yscrollcommand=self.scrollbar.set
        )
        self.scrollbar.configure(command=self.tree.yview)

        # Başlık ve Sütun Ayarları
        headings = {
            "plaka": "Araç Plaka",
            "musteri": "Müşteri Adı",
            "baslangic": "Başl. Tarihi",
            "bitis": "Bitiş Tarihi",
            "gun_sayisi": "Gün",
            "gunluk_ucret": "G. Ücret",
            "toplam_ucret": "Toplam Tutar",
            "created_at": "İşlem Zamanı"
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            # Sütun genişliklerini içeriğe göre ayarlayalım
            width = 100 if col in ["gun_sayisi", "gunluk_ucret"] else 130
            self.tree.column(col, width=width, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Alt Bilgi Çubuğu (Toplam Kayıt Sayısı İçin)
        self.footer_label = ctk.CTkLabel(self, text="", font=("Roboto", 12, "italic"))
        self.footer_label.pack(pady=(0, 10))

        self.load_history()

    def load_history(self):
        # Tabloyu temizle
        self.tree.delete(*self.tree.get_children())

        rentals = load_rentals()
        for r in rentals:
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

        self.footer_label.configure(text=f"Toplam {len(rentals)} kiralama kaydı bulundu.")