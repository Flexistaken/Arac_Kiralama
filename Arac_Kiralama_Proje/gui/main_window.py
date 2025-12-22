import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

# Servis ve Pencere Importları
from services.car_service import get_all_cars, return_car_by_plate, delete_car
from gui.add_car_window import AddCarWindow
from gui.rent_window import RentWindow
from gui.edit_car_window import EditCarWindow
from gui.rental_history_window import RentalHistoryWindow

# Görünüm Ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Araç Kiralama Sistemi v2.0")
        self.root.geometry("1100x650")

        # --- Stil Yapılandırması (Treeview'ı Modernleştirme) ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=35,  # Satırları genişlettik
                        fieldbackground="#2a2d2e",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])  # Seçili satır rengi
        style.configure("Treeview.Heading",
                        background="#1f1f1f",
                        foreground="white",
                        relief="flat",
                        font=("Roboto", 11, "bold"))

        # --- ARAMA VE FİLTRE PANELİ ---
        self.search_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.search_frame.pack(pady=20, padx=20, fill="x")

        # Arama Kutusu (Placeholder özelliği CTK'da dahili olarak var)
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.load_cars())

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            textvariable=self.search_var,
            placeholder_text="Plaka, Marka veya Model ara...",
            width=350,
            height=40,
            corner_radius=10
        )
        self.search_entry.pack(side="left", padx=20, pady=15)

        # Durum Filtresi
        ctk.CTkLabel(self.search_frame, text="Durum Filtresi:", font=("Roboto", 12)).pack(side="left", padx=(10, 5))

        self.filter_var = ctk.StringVar(value="tümü")
        self.filter_menu = ctk.CTkOptionMenu(
            self.search_frame,
            variable=self.filter_var,
            values=["tümü", "müsait", "kirada"],
            command=lambda x: self.load_cars(),
            width=120,
            corner_radius=10
        )
        self.filter_menu.pack(side="left", padx=10)

        # --- TABLO ALANI ---
        self.table_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.create_table()

        # --- BUTON PANELİ ---
        self.button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.button_frame.pack(pady=20, padx=20, fill="x")

        # Buton tasarımları için ortak özellikler
        btn_font = ("Roboto", 13, "bold")

        # Sol Taraf: Yönetim Butonları
        self.add_btn = ctk.CTkButton(self.button_frame, text="+ Araç Ekle", command=self.open_add_car_window,
                                     fg_color="#2ecc71", hover_color="#27ae60", font=btn_font)
        self.add_btn.pack(side="left", padx=5)

        self.edit_btn = ctk.CTkButton(self.button_frame, text="Düzenle", command=self.open_edit_car_window,
                                      fg_color="#f39c12", hover_color="#e67e22", font=btn_font)
        self.edit_btn.pack(side="left", padx=5)

        self.delete_btn = ctk.CTkButton(self.button_frame, text="Sil", command=self.delete_selected_car,
                                        fg_color="#e74c3c", hover_color="#c0392b", font=btn_font)
        self.delete_btn.pack(side="left", padx=5)

        # Sağ Taraf: İşlem Butonları
        self.history_btn = ctk.CTkButton(self.button_frame, text="Kiralama Geçmişi",
                                         command=lambda: RentalHistoryWindow(self.root),
                                         fg_color="#34495e", font=btn_font)
        self.history_btn.pack(side="right", padx=5)

        self.return_btn = ctk.CTkButton(self.button_frame, text="İade Al", command=self.return_car,
                                        fg_color="#9b59b6", font=btn_font)
        self.return_btn.pack(side="right", padx=5)

        self.rent_btn = ctk.CTkButton(self.button_frame, text="Kiralama Başlat", command=self.open_rent_window,
                                      font=btn_font)
        self.rent_btn.pack(side="right", padx=5)

        self.load_cars()

    def create_table(self):
        # Treeview Scrollbar ile beraber
        self.scrollbar = ctk.CTkScrollbar(self.table_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            self.table_frame,
            columns=("plaka", "marka", "model", "ucret", "durum"),
            show="headings",
            yscrollcommand=self.scrollbar.set
        )
        self.scrollbar.configure(command=self.tree.yview)

        # Başlıklar
        headers = {"plaka": "Plaka", "marka": "Marka", "model": "Model", "ucret": "Günlük Ücret", "durum": "Durum"}
        for col, text in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=150, anchor="center")

        # Renkli etiketler (Yeşil/Kırmızı)
        self.tree.tag_configure("müsait", foreground="#2ecc71")
        self.tree.tag_configure("kirada", foreground="#e74c3c")

        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

    def load_cars(self):
        self.tree.delete(*self.tree.get_children())
        search_text = self.search_var.get().lower().strip()
        filter_status = self.filter_var.get()

        for car in get_all_cars():
            # Filtreleme mantığı
            if search_text and not any(search_text in str(car[k]).lower() for k in ["plaka", "marka", "model"]):
                continue
            if filter_status != "tümü" and car["durum"] != filter_status:
                continue

            tag = "müsait" if car["durum"] == "müsait" else "kirada"
            self.tree.insert("", "end", values=(
                car["plaka"], car["marka"], car["model"], f"{car['ucret']} ₺", car["durum"].capitalize()
            ), tags=(tag,))

    # Mantıksal fonksiyonları (delete, rent, return, edit) aynen koruyabilirsin.
    # Sadece 'messagebox' CustomTkinter'da standart tkinter'dan gelir, görseli CTK değildir.
    # İstersen CTKMessagebox (dış kütüphane) kullanarak onları da modernize edebiliriz.

    def open_add_car_window(self):
        AddCarWindow(self.root, self.refresh_table)

    def refresh_table(self):
        self.load_cars()

    def delete_selected_car(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Hata", "Lütfen bir araç seçin.")
            return

        plaka = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Onay", f"{plaka} plakalı araç silinecek. Emin misiniz?"):
            delete_car(plaka)
            self.load_cars()

    def open_rent_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Hata", "Lütfen bir araç seçin.")
            return

        values = self.tree.item(selected[0])["values"]
        plaka = values[0]
        ucret = int(values[3].replace(" ₺", ""))

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
        if not selected: return
        plaka = self.tree.item(selected[0])["values"][0]
        if return_car_by_plate(plaka):
            messagebox.showinfo("Başarılı", "Araç iade alındı.")
            self.load_cars()

    def open_edit_car_window(self):
        selected = self.tree.selection()
        if not selected: return
        plaka = self.tree.item(selected[0])["values"][0]
        for car in get_all_cars():
            if car["plaka"] == plaka:
                EditCarWindow(self.root, car, self.refresh_table)
                break