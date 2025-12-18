import tkinter as tk
from tkinter import ttk
from services.car_service import get_all_cars, rent_car, return_car_by_plate, delete_car
from gui.add_car_window import AddCarWindow
from tkinter import messagebox
from gui.rent_window import RentWindow

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Araç Kiralama Sistemi")
        self.root.geometry("800x400")

        self.create_table()
        self.load_cars()

        tk.Button(
            self.root,
            text="Araç Ekle",
            command=self.open_add_car_window
            ).pack(pady=5)
        
        tk.Button(
            self.root,
            text="Sil",
            command=self.delete_selected_car
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Kiralama Başlat",
            command=self.open_rent_window
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Aracı İade Et",
            command=self.return_car
        ).pack(pady=5)

    
    def open_add_car_window(self):
        AddCarWindow(self.root, self.refresh_table)
    
    def delete_selected_car(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("Hata!", "Lütfen silinecek aracı seçiniz.")
            return

        values = self.tree.item(selected_item)["values"]
        plaka = values[0]

        confirm = messagebox.askyesno(
        "Onay",
        f"{plaka} plakalı araç silinsin mi?"
        )

        if confirm:
            delete_car(plaka)
            self.refresh_table()
            messagebox.showinfo("Başarılı!", "Araç silindi.")
    
    def open_rent_window(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("Hata!", "Lütfen bir araç seçiniz.")
            return

        values = self.tree.item(selected_item)["values"]
        plaka = values[0]
        ucret = int(values[3])
        durum = values[4]

        if durum != "müsait":
            messagebox.showerror("Hata!", "Bu araç şu an müsait değil.")
            return

        RentWindow(self.root, plaka, ucret, self.refresh_table)
    
    def return_car(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Uyarı!", "Lütfen bir araç seçiniz.")
            return

        values = self.tree.item(selected[0], "values")
        plaka = values[0]

        success = return_car_by_plate(plaka)

        if success:
            messagebox.showinfo("Başarılı!", "Araç iade edildi.")
            self.load_cars()
        else:
            messagebox.showwarning("Uyarı!", "Bu araç zaten müsait.")


    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.load_cars()

    def create_table(self):
        columns = ("plaka", "marka", "model", "ucret", "durum")

        self.tree = ttk.Treeview(
            self.root,
            columns=("plaka", "marka", "model", "ucret", "durum"),
            show="headings",
            height=10
        )

        self.tree.column("plaka", width=100)
        self.tree.column("marka", width=100)
        self.tree.column("model", width=100)
        self.tree.column("ucret", width=80)
        self.tree.column("durum", width=80)


        self.tree.heading("plaka", text="Plaka")
        self.tree.heading("marka", text="Marka")
        self.tree.heading("model", text="Model")
        self.tree.heading("ucret", text="Günlük Ücret")
        self.tree.heading("durum", text="Durum")

        self.tree.tag_configure("müsait", foreground="green")
        self.tree.tag_configure("kirada", foreground="red")

        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_cars(self):
        cars = get_all_cars()

        self.tree.delete(*self.tree.get_children())

        for car in cars:
            tag = "müsait" if car["durum"] == "müsait" else "kirada"

            durum_gosterim = (
                "● Müsait" if car["durum"] == "müsait" else "● Kirada"
            )

            self.tree.insert(
                "",
                tk.END,
                values=(
                    car["plaka"],
                    car["marka"],
                    car["model"],
                    car["ucret"],
                    durum_gosterim
                ),
                tags=(tag,)
        )
