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

        # =========================
        # 1️⃣ ARAMA + FİLTRE ALANI
        # =========================
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Ara:").pack(side=tk.LEFT, padx=5)

        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="tümü")

        # Arama kutusu placeholder ile
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=25,
            fg="grey"
        )
        self.search_entry.pack(side=tk.LEFT)
        self.placeholder_text = "Plaka / Marka / Model ara..."
        self.search_var.set(self.placeholder_text)


        tk.Label(search_frame, text="Durum:").pack(side=tk.LEFT, padx=5)

        filter_menu = ttk.Combobox(
            search_frame,
            textvariable=self.filter_var,
            values=["tümü", "müsait", "kirada"],
            state="readonly",
            width=10
        )
        filter_menu.pack(side=tk.LEFT)

        # 🔥 trace_add MUTLAKA burada
        self.search_var.trace_add("write", lambda *args: self.load_cars())
        self.filter_var.trace_add("write", lambda *args: self.load_cars())
        self.search_entry.bind("<FocusIn>", self.on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_search_focus_out)


        # =========================
        # 2️⃣ TABLO
        # =========================
        self.create_table()

        # =========================
        # 3️⃣ BUTONLAR
        # =========================
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

        # =========================
        # 4️⃣ 🔥 EN SON: VERİYİ YÜKLE
        # =========================
        self.load_cars()




    
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
    
    def on_search_focus_in(self, event):
        if self.search_var.get() == self.placeholder_text:
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="black")

    def on_search_focus_out(self, event):
        if not self.search_var.get().strip():
            self.search_var.set(self.placeholder_text)
            self.search_entry.config(fg="grey")


    def load_cars(self):
        self.tree.delete(*self.tree.get_children())

        search_text = self.search_var.get().strip()

        if search_text == self.placeholder_text:
            search_text = ""
        else:
            search_text = search_text.lower()

        filter_status = self.filter_var.get()

        for car in get_all_cars():

        # 🔍 ARAMA (plaka / marka / model)
            if search_text:
                if not (
                    search_text in car["plaka"].lower()
                    or search_text in car["marka"].lower()
                    or search_text in car["model"].lower()
                ):
                    continue

        # 🔎 FİLTRELEME (durum)
            if filter_status != "tümü" and car["durum"] != filter_status:
                continue

            tag = "müsait" if car["durum"] == "müsait" else "kirada"
            durum_gosterim = "Müsait" if car["durum"] == "müsait" else "Kirada"

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
