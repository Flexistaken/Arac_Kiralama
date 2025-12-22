import customtkinter as ctk
from tkinter import messagebox
from models.car import Car
from services.car_service import add_car
from utils.validators import is_empty, is_number

# Görünüm Ayarları (Uygulamanın ana dosyasında bir kez yapılması yeterlidir ama burada da durabilir)
ctk.set_appearance_mode("dark")  # "dark" veya "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


class AddCarWindow(ctk.CTkToplevel):  # tk.Toplevel yerine ctk.CTkToplevel
    def __init__(self, parent, refresh_callback):
        super().__init__(parent)

        self.refresh_callback = refresh_callback
        self.title("Araç Ekle")
        self.geometry("340x450")

        # Pencereyi diğer pencerelerin önünde tutar
        self.attributes("-topmost", True)

        # Ana Başlık
        self.header_label = ctk.CTkLabel(self, text="Yeni Araç Bilgileri", font=("Roboto", 20, "bold"))
        self.header_label.pack(pady=(20, 10))

        # --- Girdi Alanları ---
        # Her biri için ortak ayarları (genişlik, köşe yuvarlaklığı) kullanıyoruz
        entry_width = 250
        entry_corner = 10

        self.plaka_entry = ctk.CTkEntry(self, placeholder_text="Plaka (Örn: 34ABC123)", width=entry_width,
                                        corner_radius=entry_corner)
        self.plaka_entry.pack(pady=10)

        self.marka_entry = ctk.CTkEntry(self, placeholder_text="Marka (Örn: BMW)", width=entry_width,
                                        corner_radius=entry_corner)
        self.marka_entry.pack(pady=10)

        self.model_entry = ctk.CTkEntry(self, placeholder_text="Model (Örn: 3.20i)", width=entry_width,
                                        corner_radius=entry_corner)
        self.model_entry.pack(pady=10)

        self.ucret_entry = ctk.CTkEntry(self, placeholder_text="Günlük Ücret (₺)", width=entry_width,
                                        corner_radius=entry_corner)
        self.ucret_entry.pack(pady=10)

        # --- Kaydet Butonu ---
        self.save_button = ctk.CTkButton(
            self,
            text="Aracı Kaydet",
            command=self.save_car,
            width=entry_width,
            height=40,
            corner_radius=20,
            font=("Roboto", 14, "bold"),
            fg_color="#1f6aa5",  # Butonun ana rengi
            hover_color="#144870"  # Üzerine gelince renk değişimi
        )
        self.save_button.pack(pady=(30, 20))

    def save_car(self):
        plaka = self.plaka_entry.get().strip().upper()
        raw_marka = self.marka_entry.get().strip()
        raw_model = self.model_entry.get().strip()

        marka = raw_marka if raw_marka.isupper() else raw_marka.title()
        model = raw_model if raw_model.isupper() else raw_model.title()
        ucret = self.ucret_entry.get().strip()

        # Doğrulamalar
        if is_empty(plaka, marka, model, ucret):
            messagebox.showerror("Hata!", "Lütfen tüm alanları doldurun.")
            return

        if not is_number(ucret):
            messagebox.showerror("Hata!", "Ücret alanına sadece sayı girmelisiniz.")
            return

        # Veritabanına/Servise ekleme
        car = Car(plaka, marka, model, int(ucret))
        add_car(car.to_dict())

        messagebox.showinfo("Başarılı!", f"{plaka} plakalı araç başarıyla eklendi.")
        self.refresh_callback()
        self.destroy()  # Pencereyi kapat