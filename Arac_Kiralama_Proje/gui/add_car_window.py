import customtkinter as ctk
from tkinter import messagebox
from models.car import Car
# get_all_cars fonksiyonunu kontrol işlemi için import ediyoruz
from services.car_service import add_car, get_all_cars
from utils.validators import is_empty, is_number


class AddCarWindow(ctk.CTkToplevel):
    def __init__(self, parent, refresh_callback):
        super().__init__(parent)

        self.refresh_callback = refresh_callback
        self.title("Araç Ekle")
        self.geometry("340x480")
        self.attributes("-topmost", True)

        # Başlık
        self.header_label = ctk.CTkLabel(self, text="Yeni Araç Bilgileri", font=("Roboto", 20, "bold"))
        self.header_label.pack(pady=(20, 10))

        # Giriş Alanları
        entry_width = 250
        self.plaka_entry = ctk.CTkEntry(self, placeholder_text="Plaka (Örn: 34ABC123)", width=entry_width)
        self.plaka_entry.pack(pady=10)

        self.marka_entry = ctk.CTkEntry(self, placeholder_text="Marka", width=entry_width)
        self.marka_entry.pack(pady=10)

        self.model_entry = ctk.CTkEntry(self, placeholder_text="Model", width=entry_width)
        self.model_entry.pack(pady=10)

        self.ucret_entry = ctk.CTkEntry(self, placeholder_text="Günlük Ücret (₺)", width=entry_width)
        self.ucret_entry.pack(pady=10)

        # Kaydet Butonu
        self.save_button = ctk.CTkButton(
            self,
            text="Aracı Kaydet",
            command=self.save_car,
            width=entry_width,
            height=40,
            font=("Roboto", 14, "bold")
        )
        self.save_button.pack(pady=(30, 20))

    def save_car(self):
        plaka = self.plaka_entry.get().strip().upper()
        raw_marka = self.marka_entry.get().strip()
        raw_model = self.model_entry.get().strip()
        ucret = self.ucret_entry.get().strip()

        # 1. Boşluk Kontrolü
        if is_empty(plaka, raw_marka, raw_model, ucret):
            messagebox.showerror("Hata!", "Lütfen tüm alanları doldurun.")
            return

        # 2. Plaka Çakışma Kontrolü (Yeni Eklenen Kısım)
        mevcut_araclar = get_all_cars()
        for arac in mevcut_araclar:
            if arac["plaka"].upper() == plaka:
                messagebox.showerror("Hata!", f"{plaka} plakalı araç zaten sistemde kayıtlı.")
                return

        # 3. Sayısal Kontrol
        if not is_number(ucret):
            messagebox.showerror("Hata!", "Ücret alanına sadece sayı girmelisiniz.")
            return

        # Kayıt İşlemi
        marka = raw_marka if raw_marka.isupper() else raw_marka.title()
        model = raw_model if raw_model.isupper() else raw_model.title()

        car = Car(plaka, marka, model, int(ucret))
        add_car(car.to_dict())

        messagebox.showinfo("Başarılı!", f"{plaka} plakalı araç sisteme eklendi.")
        self.refresh_callback()
        self.destroy()