import tkinter as tk
from tkinter import messagebox
from services.car_service import update_car

class EditCarWindow:
    def __init__(self, parent, car, refresh_callback):
        self.car = car
        self.refresh_callback = refresh_callback
        self.old_status = car["durum"]


        self.window = tk.Toplevel(parent)
        self.window.title("Araç Düzenle")
        self.window.geometry("300x300")

        # Plaka değiştirilemez.
        tk.Label(self.window, text="Plaka").pack()
        self.plaka_entry = tk.Entry(self.window)
        self.plaka_entry.pack()
        self.plaka_entry.insert(0, car["plaka"])
        self.plaka_entry.config(state="disabled")

        # Marka
        tk.Label(self.window, text="Marka").pack()
        self.marka_entry = tk.Entry(self.window)
        self.marka_entry.pack()
        self.marka_entry.insert(0, car["marka"])

        # Model
        tk.Label(self.window, text="Model").pack()
        self.model_entry = tk.Entry(self.window)
        self.model_entry.pack()
        self.model_entry.insert(0, car["model"])

        # Ücret
        tk.Label(self.window, text="Günlük Ücret").pack()
        self.ucret_entry = tk.Entry(self.window)
        self.ucret_entry.pack()
        self.ucret_entry.insert(0, car["ucret"])

        # Durum
        tk.Label(self.window, text="Durum").pack()
        self.durum_var = tk.StringVar(value=car["durum"])
        tk.OptionMenu(
            self.window,
            self.durum_var,
            "müsait",
            "kirada"
        ).pack()

        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Kaydet",
            command=self.save_changes
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="İptal",
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)


    def save_changes(self):
        try:
            self.car["marka"] = self.marka_entry.get()
            self.car["model"] = self.model_entry.get()
            self.car["ucret"] = int(self.ucret_entry.get())
            self.car["durum"] = self.durum_var.get()

            new_status = self.durum_var.get()

            # Eğer müsaitten kirada yapıldıysa rent window açma
            if self.old_status == "müsait" and new_status == "kirada":
                self.window.destroy()
                from gui.rent_window import RentWindow
                RentWindow(self.window.master, self.car["plaka"], self.car["ucret"], self.refresh_callback)
                return
            
            update_car(self.car)
            messagebox.showinfo("Başarılı", "Araç güncellendi.")
            self.refresh_callback()
            self.window.destroy()

        except ValueError:
            messagebox.showerror("Hata", "Günlük ücret sayısal olmalıdır.")
