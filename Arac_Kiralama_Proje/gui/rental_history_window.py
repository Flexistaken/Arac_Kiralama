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
                        rowheight=45,
                        fieldbackground="#2a2d2e",
                        borderwidth=0,
                        font=("Roboto", 14))
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

                # --- TARİH BAZLI ARAMA PANELİ ---
        self.search_frame = ctk.CTkFrame(self, corner_radius=15)
        self.search_frame.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(
            self.search_frame,
            text="Tarihe Göre Ara:",
            font=("Roboto", 14, "bold")
        ).pack(side="left", padx=(15, 10), pady=12)

        self.date_search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="YYYY-AA-GG veya YYYY-AA (örn: 2026-01)",
            placeholder_text_color="gray70",
            width=420,
            height=40,
            corner_radius=10,
            font=("Roboto", 13)
        )
        self.date_search_entry.pack(side="left", padx=(0, 10), pady=12)

        # Yazdıkça ara
        self.date_search_entry.bind("<KeyRelease>", lambda e: self.load_history())

        self.clear_btn = ctk.CTkButton(
            self.search_frame,
            text="Temizle",
            width=90,
            height=40,
            command=self.clear_search
        )
        self.clear_btn.pack(side="left", pady=12)

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
        self.tree.delete(*self.tree.get_children())
        rentals = load_rentals()
        query = self.date_search_entry.get().strip()

        # 🔒 KORUMA: Tarih yazılmadıysa filtreleme yapma
        if len(query) >= 4:  # en az "2024"
            rentals = [
                r for r in rentals
                if query in str(r.get("baslangic", ""))
                or query in str(r.get("bitis", ""))
                or query in str(r.get("created_at", ""))
            ]

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

        self.footer_label.configure(
            text=f"Toplam {len(rentals)} kiralama kaydı bulundu."
        )


        
    def clear_search(self):
        self.date_search_entry.delete(0, tk.END)
        self.load_history()
