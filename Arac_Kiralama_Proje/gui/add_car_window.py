import tkinter as tk
from tkinter import messagebox
from models.car import Car
from services.car_service import add_car
from utils.validators import is_empty, is_number

class AddCarWindow:
    def __init__(self, parent, refresh_callback):
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Araç Ekle")
        self.window.geometry("300x300")

        tk.Label(self.window, text="Plaka").pack()
        self.plaka_entry = tk.Entry(self.window)
        self.plaka_entry.pack()

        tk.Label(self.window, text="Marka").pack()
        self.marka_entry = tk.Entry(self.window)
        self.marka_entry.pack()

        tk.Label(self.window, text="Model").pack()
        self.model_entry = tk.Entry(self.window)
        self.model_entry.pack()

        tk.Label(self.window, text="Günlük Ücret").pack()
        self.ucret_entry = tk.Entry(self.window)
        self.ucret_entry.pack()

        tk.Button(self.window, text="Kaydet", command=self.save_car).pack(pady=10)

    def save_car(self):
        plaka = self.plaka_entry.get()
        marka = self.marka_entry.get()
        model = self.model_entry.get()
        ucret = self.ucret_entry.get()

        if is_empty(plaka, marka, model, ucret):
            messagebox.showerror("Hata", "Boş alan bırakılamaz")
            return

        if not is_number(ucret):
            messagebox.showerror("Hata", "Ücret sayısal olmalıdır")
            return

        car = Car(plaka, marka, model, int(ucret))
        add_car(car.to_dict())

        messagebox.showinfo("Başarılı", "Araç eklendi")
        self.refresh_callback()
        self.window.destroy()
