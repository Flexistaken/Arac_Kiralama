import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

# Servis ve Diğer Pencere Importları
from services.car_service import get_all_cars, return_car_by_plate, delete_car
from gui.add_car_window import AddCarWindow
from gui.rent_window import RentWindow
from gui.edit_car_window import EditCarWindow
from gui.rental_history_window import RentalHistoryWindow


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Araç Kiralama Sistemi v2.0")
        self.root.geometry("1200x700")  # Yazılar büyüdüğü için pencereyi biraz genişlettik

        # --- MODERN STİL YAPILANDIRMASI ---
        style = ttk.Style()
        style.theme_use("default")

        # Tablo İçeriği (Yazı boyutunu 14 yaptık)
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=45,  # Satır yüksekliğini yazı boyutuna göre artırdık
                        fieldbackground="#2a2d2e",
                        borderwidth=0,
                        font=("Roboto", 14))  # Marka ve modeller burada büyüyor

        style.map('Treeview', background=[('selected', '#1f538d')])

        # Tablo Başlıkları
        style.configure("Treeview.Heading",
                        background="#1f1f1f",
                        foreground="white",
                        relief="flat",
                        font=("Roboto", 13, "bold"))

        # --- 1. ÜST PANEL: ARAMA VE FİLTRELEME ---
        self.search_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.search_frame.pack(pady=20, padx=20, fill="x")

        # Arama Kutusu
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.load_cars())

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            textvariable=self.search_var,
            placeholder_text="Plaka, Marka veya Model ara...",
            width=400,
            height=45,
            corner_radius=10,
            font=("Roboto", 14)
        )
        self.search_entry.pack(side="left", padx=20, pady=15)

        # Durum Filtresi
        ctk.CTkLabel(self.search_frame, text="Durum:", font=("Roboto", 14, "bold")).pack(side="left", padx=(10, 5))

        self.filter_var = ctk.StringVar(value="tümü")
        self.filter_menu = ctk.CTkOptionMenu(
            self.search_frame,
            variable=self.filter_var,
            values=["tümü", "müsait", "kirada"],
            command=lambda x: self.load_cars(),
            width=140,
            height=35,
            corner_radius=10
        )
        self.filter_menu.pack(side="left", padx=10)

        # --- 2. ORTA PANEL: ARAÇ TABLOSU ---
        self.table_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.table_frame.pack(pady=5, padx=20, fill="both", expand=True)

        self.create_table()

        # --- 3. ALT PANEL: İŞLEM BUTONLARI ---
        self.button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.button_frame.pack(pady=25, padx=20, fill="x")

        btn_font = ("Roboto", 14, "bold")

        # Sol Grup: Yönetim İşlemleri
        self.add_btn = ctk.CTkButton(self.button_frame, text="+ Araç Ekle", command=self.open_add_car_window,
                                     fg_color="#2ecc71", hover_color="#27ae60", font=btn_font, height=45)
        self.add_btn.pack(side="left", padx=5)

        self.edit_btn = ctk.CTkButton(self.button_frame, text="Düzenle", command=self.open_edit_car_window,
                                      fg_color="#f39c12", hover_color="#e67e22", font=btn_font, height=45)
        self.edit_btn.pack(side="left", padx=5)

        self.delete_btn = ctk.CTkButton(self.button_frame, text="Sil", command=self.delete_selected_car,
                                        fg_color="#e74c3c", hover_color="#c0392b", font=btn_font, height=45)
        self.delete_btn.pack(side="left", padx=5)

        # Sağ Grup: Kiralama İşlemleri
        self.history_btn = ctk.CTkButton(self.button_frame, text="Kiralama Geçmişi",
                                         command=lambda: RentalHistoryWindow(self.root),
                                         fg_color="#34495e", font=btn_font, height=45)
        self.history_btn.pack(side="right", padx=5)

        self.return_btn = ctk.CTkButton(self.button_frame, text="İade Al", command=self.return_car,
                                        fg_color="#9b59b6", font=btn_font, height=45)
        self.return_btn.pack(side="right", padx=5)

        self.rent_btn = ctk.CTkButton(self.button_frame, text="Kiralama Başlat", command=self.open_rent_window,
                                      font=btn_font, height=45)
        self.rent_btn.pack(side="right", padx=5)

        # İlk veri yüklemesi
        self.load_cars()

    def create_table(self):
        # Modern Kaydırma Çubuğu
        self.scrollbar = ctk.CTkScrollbar(self.table_frame)
        self.scrollbar.pack(side="right", fill="y", padx=2, pady=2)

        self.tree = ttk.Treeview(
            self.table_frame,
            columns=("plaka", "marka", "model", "ucret", "durum"),
            show="headings",
            yscrollcommand=self.scrollbar.set
        )
        self.scrollbar.configure(command=self.tree.yview)

        # Sütun Tanımlamaları
        columns = {
            "plaka": ("Plaka", 150),
            "marka": ("Marka", 200),
            "model": ("Model", 200),
            "ucret": ("Günlük Ücret", 150),
            "durum": ("Durum", 150)
        }

        for col, (text, width) in columns.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="center")

        # Duruma göre renk etiketleri
        self.tree.tag_configure("müsait", foreground="#2ecc71")
        self.tree.tag_configure("kirada", foreground="#e74c3c")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    def load_cars(self):
        self.tree.delete(*self.tree.get_children())
        search_text = self.search_var.get().lower().strip()
        filter_status = self.filter_var.get()

        for car in get_all_cars():
            # Arama filtresi
            if search_text and not any(search_text in str(car[k]).lower() for k in ["plaka", "marka", "model"]):
                continue

            # Durum filtresi
            if filter_status != "tümü" and car["durum"] != filter_status:
                continue

            tag = "müsait" if car["durum"] == "müsait" else "kirada"
            self.tree.insert("", "end", values=(
                car["plaka"],
                car["marka"],
                car["model"],
                f"{car['ucret']} ₺",
                car["durum"].capitalize()
            ), tags=(tag,))

    def refresh_table(self):
        self.load_cars()

    def open_add_car_window(self):
        AddCarWindow(self.root, self.refresh_table)

    def delete_selected_car(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen silinecek aracı seçin.")
            return

        plaka = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Onay", f"{plaka} plakalı araç silinecek. Emin misiniz?"):
            delete_car(plaka)
            self.load_cars()

    def open_rent_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen kiralanacak aracı seçin.")
            return

        values = self.tree.item(selected[0])["values"]
        plaka = values[0]
        ucret_str = values[3].replace(" ₺", "")
        ucret = int(ucret_str)

        # Müsaitlik kontrolü
        for car in get_all_cars():
            if car["plaka"] == plaka:
                if car["durum"] != "müsait":
                    messagebox.showerror("Hata", "Bu araç zaten kirada!")
                    return
                break

        RentWindow(self.root, plaka, ucret, self.refresh_table)

    def return_car(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen iade edilecek aracı seçin.")
            return

        plaka = self.tree.item(selected[0])["values"][0]
        if return_car_by_plate(plaka):
            messagebox.showinfo("Başarılı", "Araç iade alındı.")
            self.load_cars()
        else:
            messagebox.showwarning("Uyarı", "Bu araç zaten müsait durumda.")

    def open_edit_car_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen düzenlenecek aracı seçin.")
            return

        plaka = self.tree.item(selected[0])["values"][0]
        for car in get_all_cars():
            if car["plaka"] == plaka:
                EditCarWindow(self.root, car, self.refresh_table)
                break