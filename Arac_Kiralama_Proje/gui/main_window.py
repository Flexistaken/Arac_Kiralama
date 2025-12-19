import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from services.car_service import get_all_cars, return_car_by_plate, delete_car
from gui.add_car_window import AddCarWindow
from gui.rent_window import RentWindow
from gui.edit_car_window import EditCarWindow
from gui.rental_history_window import RentalHistoryWindow


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Araç Kiralama Sistemi")
        self.root.geometry("1000x550")

        #arama ve filtre

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

        # trace_add
        self.search_var.trace_add("write", lambda *args: self.load_cars())
        self.filter_var.trace_add("write", lambda *args: self.load_cars())
        self.search_entry.bind("<FocusIn>", self.on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_search_focus_out)


        self.create_table()

        #button frame ve butonlar

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)


        tk.Button(
            button_frame,
            text="Araç Ekle",
            command=self.open_add_car_window
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Sil",
            command=self.delete_selected_car
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Kiralama Başlat",
            command=self.open_rent_window
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Aracı İade Et",
            command=self.return_car
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Araç Düzenle",
            command=self.open_edit_car_window
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Kiralama Geçmişi",
            command=lambda: RentalHistoryWindow(self.root)
        ).pack(side=tk.LEFT, padx=5)



        # en sonda load
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
        ucret = int(values[3].split()[0])

        # müsait, kirada'yı gui'da değiştirdiğimiz için gui'dan bakıp hatayı vermek yerine plaka'dan müsaitlik durumuna bakıyor.
        for car in get_all_cars():
            if car["plaka"] == plaka:
                if car["durum"] != "müsait":
                    messagebox.showerror("Hata!", "Bu araç şu an müsait değil.")
                    return
                break

        # müsait olunca rent windowu açılır
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
        
    def open_edit_car_window(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showerror("Hata!", "Lütfen düzenlenecek aracı seçiniz.")
            return

        values = self.tree.item(selected[0])["values"]
        plaka = values[0]

        # gerçek veriyi servisten al
        for car in get_all_cars():
            if car["plaka"] == plaka:
                EditCarWindow(self.root, car, self.refresh_table)
                break



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

        # filtreleme işi
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
                    f'{car["ucret"]} ₺', # ücret kısmına tl işareti ekledim
                    durum_gosterim
                ),
                tags=(tag,)
            )
