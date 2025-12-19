import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from services.car_service import rent_car
from utils.validators import is_empty, is_valid_date, is_date_order_valid

class RentWindow:
    def __init__(self, parent, plaka, gunluk_ucret, refresh_callback):
        self.plaka = plaka
        self.gunluk_ucret = gunluk_ucret
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Araç Kiralama")
        self.window.geometry("300x300")

        tk.Label(self.window, text=f"Plaka: {plaka}").pack(pady=5)

        tk.Label(self.window, text="Müşteri Adı").pack()
        self.musteri_entry = tk.Entry(self.window)
        self.musteri_entry.pack()

        tk.Label(self.window, text="Başlangıç Tarihi (YYYY-MM-DD)").pack()
        self.baslangic_entry = tk.Entry(self.window)
        self.baslangic_entry.pack()

        tk.Label(self.window, text="Bitiş Tarihi (YYYY-MM-DD)").pack()
        self.bitis_entry = tk.Entry(self.window)
        self.bitis_entry.pack()

        self.total_label = tk.Label(self.window, text="Toplam Ücret: -")
        self.total_label.pack(pady=10)

        tk.Button(self.window, text="Hesapla", command=self.calculate_price).pack()
        tk.Button(self.window, text="Kaydet", command=self.save_rent).pack(pady=10)

    def calculate_price(self):
        start = self.baslangic_entry.get()
        end = self.bitis_entry.get()

        if not is_valid_date(start) or not is_valid_date(end):
            messagebox.showerror("Hata!", "Tarih formatı yanlış.")
            return

        if not is_date_order_valid(start, end):
            messagebox.showerror("Hata!", "Bitiş tarihi başlangıçtan önce olamaz.")
            return

        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        gun = (end_date - start_date).days + 1
        toplam = gun * self.gunluk_ucret

        self.total_label.config(text=f"Toplam Ücret: {toplam} ₺")

    def save_rent(self):
        musteri = self.musteri_entry.get()
        baslangic = self.baslangic_entry.get()
        bitis = self.bitis_entry.get()

        if is_empty(musteri, baslangic, bitis):
            messagebox.showerror("Hata!", "Boş alan bırakılamaz.")
            return

        if not is_valid_date(baslangic) or not is_valid_date(bitis):
            messagebox.showerror("Hata!", "Tarih formatı yanlış.")
            return

        if not is_date_order_valid(baslangic, bitis):
            messagebox.showerror("Hata!", "Bitiş tarihi başlangıçtan önce olamaz.")
            return

        rent_car(self.plaka, musteri, baslangic, bitis)
        self.refresh_callback()

        messagebox.showinfo("Başarılı!", "Kiralama işlemi tamamlandı.")
        self.window.destroy()
