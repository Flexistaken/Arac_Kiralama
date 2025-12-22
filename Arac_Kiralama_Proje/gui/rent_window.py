import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date

from services.car_service import rent_car
from services.rental_service import add_rental_record
from utils.validators import is_empty, is_valid_date, is_date_order_valid


class RentWindow(ctk.CTkToplevel):
    def __init__(self, parent, plaka, gunluk_ucret, refresh_callback):
        super().__init__(parent)

        self.plaka = plaka
        self.gunluk_ucret = gunluk_ucret
        self.refresh_callback = refresh_callback

        self.title("Araç Kiralama İşlemi")
        self.geometry("380x580")
        self.attributes("-topmost", True)

        # Üst Bilgi Kartı
        self.header_frame = ctk.CTkFrame(self, fg_color="#1f538d", corner_radius=10)
        self.header_frame.pack(pady=20, padx=20, fill="x")

        ctk.CTkLabel(self.header_frame, text=f"PLAKA: {plaka}", font=("Roboto", 18, "bold"), text_color="white").pack(
            pady=10)
        ctk.CTkLabel(self.header_frame, text=f"Günlük Ücret: {gunluk_ucret} ₺", font=("Roboto", 14),
                     text_color="#ecf0f1").pack(pady=(0, 10))

        # Giriş Alanları Konfigürasyonu
        entry_width = 280
        entry_corner = 10

        # Müşteri Adı
        ctk.CTkLabel(self, text="Müşteri Adı ve Soyadı", font=("Roboto", 12, "bold")).pack(pady=(10, 0))
        self.musteri_entry = ctk.CTkEntry(self, placeholder_text="Örn: Ahmet Yılmaz", width=entry_width,
                                          corner_radius=entry_corner)
        self.musteri_entry.pack(pady=5)

        # Başlangıç Tarihi
        ctk.CTkLabel(self, text="Başlangıç Tarihi", font=("Roboto", 12, "bold")).pack(pady=(10, 0))
        self.baslangic_entry = ctk.CTkEntry(self, placeholder_text="YYYY-MM-DD (Örn: 2025-12-22)", width=entry_width,
                                            corner_radius=entry_corner)
        self.baslangic_entry.pack(pady=5)
        # Bugünü otomatik dolduralım (Kullanıcıya kolaylık)
        self.baslangic_entry.insert(0, date.today().strftime("%Y-%m-%d"))

        # Bitiş Tarihi
        ctk.CTkLabel(self, text="Bitiş Tarihi", font=("Roboto", 12, "bold")).pack(pady=(10, 0))
        self.bitis_entry = ctk.CTkEntry(self, placeholder_text="YYYY-MM-DD", width=entry_width,
                                        corner_radius=entry_corner)
        self.bitis_entry.pack(pady=5)

        # --- Toplam Ücret Göstergesi ---
        self.price_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.price_frame.pack(pady=20)

        self.total_label = ctk.CTkLabel(self.price_frame, text="Toplam Ücret: -", font=("Roboto", 20, "bold"),
                                        text_color="#2ecc71")
        self.total_label.pack()

        # --- Butonlar ---
        self.calc_button = ctk.CTkButton(
            self,
            text="Ücreti Hesapla",
            command=self.calculate_price,
            fg_color="#34495e",
            hover_color="#2c3e50",
            width=entry_width,
            height=35
        )
        self.calc_button.pack(pady=5)

        self.save_button = ctk.CTkButton(
            self,
            text="Kiralamayı Onayla",
            command=self.save_rent,
            fg_color="#27ae60",
            hover_color="#219150",
            width=entry_width,
            height=45,
            font=("Roboto", 14, "bold")
        )
        self.save_button.pack(pady=20)

    def calculate_price(self):
        start = self.baslangic_entry.get()
        end = self.bitis_entry.get()

        if not is_valid_date(start) or not is_valid_date(end):
            messagebox.showerror("Hata!", "Tarih formatı yanlış (YYYY-MM-DD olmalı).")
            return

        if not is_date_order_valid(start, end):
            messagebox.showerror("Hata!", "Dönüş tarihi başlangıçtan önce olamaz.")
            return

        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        gun = (end_date - start_date).days + 1
        toplam = gun * self.gunluk_ucret

        self.total_label.configure(text=f"Toplam Ücret: {toplam} ₺")
        return toplam  # Kaydetme işlemi için lazım olabilir

    def save_rent(self):
        musteri = self.musteri_entry.get().strip()
        baslangic = self.baslangic_entry.get().strip()
        bitis = self.bitis_entry.get().strip()

        if is_empty(musteri, baslangic, bitis):
            messagebox.showerror("Hata!", "Lütfen tüm alanları doldurun.")
            return

        # Tarih ve mantık kontrolleri (Mevcut mantığını koruyoruz)
        if not is_valid_date(baslangic) or not is_valid_date(bitis):
            messagebox.showerror("Hata!", "Tarih formatı geçersiz.")
            return

        if not is_date_order_valid(baslangic, bitis):
            messagebox.showerror("Hata!", "Tarih sıralaması hatalı.")
            return

        baslangic_date = datetime.strptime(baslangic, "%Y-%m-%d").date()
        if baslangic_date < date.today():
            messagebox.showerror("Hata!", "Geçmiş bir tarihe kiralama yapılamaz.")
            return

        # İşlemleri Gerçekleştir
        rent_car(self.plaka, musteri, baslangic, bitis)
        add_rental_record(self.plaka, musteri, baslangic, bitis, self.gunluk_ucret)

        self.refresh_callback()
        messagebox.showinfo("Başarılı", f"{self.plaka} plakalı araç {musteri} adına kiralandı.")
        self.destroy()