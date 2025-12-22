import customtkinter as ctk
from tkinter import messagebox
from services.car_service import update_car


class EditCarWindow(ctk.CTkToplevel):
    def __init__(self, parent, car, refresh_callback):
        super().__init__(parent)

        self.car = car
        self.refresh_callback = refresh_callback
        self.old_status = car["durum"]

        self.title("Araç Düzenle")
        self.geometry("360x520")
        self.attributes("-topmost", True)  # Önde kalmasını sağlar

        # Ana Başlık
        self.label_head = ctk.CTkLabel(self, text="Araç Bilgilerini Düzenle", font=("Roboto", 20, "bold"))
        self.label_head.pack(pady=(20, 10))

        # Stil Değişkenleri
        entry_width = 250
        entry_corner = 10

        # Plaka değiştirilemeyen.
        ctk.CTkLabel(self, text="Plaka (Değiştirilemez)", font=("Roboto", 12)).pack(pady=(5, 0))
        self.plaka_entry = ctk.CTkEntry(self, width=entry_width, corner_radius=entry_corner)
        self.plaka_entry.insert(0, car["plaka"])
        self.plaka_entry.configure(state="disabled", fg_color="#3d3d3d")  # Kilitli olduğu belli olsun
        self.plaka_entry.pack(pady=5)

        # Marka
        ctk.CTkLabel(self, text="Marka", font=("Roboto", 12)).pack(pady=(5, 0))
        self.marka_entry = ctk.CTkEntry(self, width=entry_width, corner_radius=entry_corner)
        self.marka_entry.insert(0, car["marka"])
        self.marka_entry.pack(pady=5)

        # Model
        ctk.CTkLabel(self, text="Model", font=("Roboto", 12)).pack(pady=(5, 0))
        self.model_entry = ctk.CTkEntry(self, width=entry_width, corner_radius=entry_corner)
        self.model_entry.insert(0, car["model"])
        self.model_entry.pack(pady=5)

        # Ücret
        ctk.CTkLabel(self, text="Günlük Ücret", font=("Roboto", 12)).pack(pady=(5, 0))
        self.ucret_entry = ctk.CTkEntry(self, width=entry_width, corner_radius=entry_corner)
        self.ucret_entry.insert(0, car["ucret"])
        self.ucret_entry.pack(pady=5)

        # Durum(müsait/kirada)
        ctk.CTkLabel(self, text="Durum", font=("Roboto", 12)).pack(pady=(5, 0))
        self.durum_menu = ctk.CTkOptionMenu(
            self,
            values=["müsait", "kirada"],
            width=entry_width,
            corner_radius=entry_corner,
            dynamic_resizing=False
        )
        self.durum_menu.set(car["durum"])
        self.durum_menu.pack(pady=10)

        # Butonlar , frame bir de
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.save_button = ctk.CTkButton(
            self.btn_frame,
            text="Güncelle",
            command=self.save_changes,
            width=120,
            corner_radius=15,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.save_button.pack(side="left", padx=10)

        self.cancel_button = ctk.CTkButton(
            self.btn_frame,
            text="İptal",
            command=self.destroy,
            width=120,
            corner_radius=15,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        self.cancel_button.pack(side="left", padx=10)

    def save_changes(self):
        try:
            self.car["marka"] = self.marka_entry.get()
            self.car["model"] = self.model_entry.get()
            self.car["ucret"] = int(self.ucret_entry.get())
            self.car["durum"] = self.durum_menu.get()

            new_status = self.durum_menu.get()

            # müsaitten kiradaya geçiş
            if self.old_status == "müsait" and new_status == "kirada":
                self.destroy()
                from gui.rent_window import RentWindow
                RentWindow(self.master, self.car["plaka"], self.car["ucret"], self.refresh_callback)
                return

            update_car(self.car)
            messagebox.showinfo("Başarılı", "Araç bilgileri güncellendi.")
            self.refresh_callback()
            self.destroy()

        except ValueError:
            messagebox.showerror("Hata", "Lütfen günlük ücret kısmına sadece sayı giriniz.")