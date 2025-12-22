import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

# Servis ve Diğer Pencere Importları
from services.car_service import get_all_cars, return_car_by_plate, delete_car
from gui.add_car_window import AddCarWindow
from gui.rent_window import RentWindow
from gui.edit_car_window import EditCarWindow
from gui.rental_history_window import RentalHistoryWindow
from gui.stats_window import StatsWindow  # Yeni eklediğimiz istatistik penceresi


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Araç Kiralama Sistemi v2.0 - Yönetim Paneli")
        self.root.geometry("1280x720")  # Daha geniş bir çalışma alanı

        # --- MODERN STİL YAPILANDIRMASI ---
        style = ttk.Style()
        style.theme_use("default")

        # Tablo İçeriği (Yazı boyutu 14, Satır yüksekliği 45)
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=45,
                        fieldbackground="#2a2d2e",
                        borderwidth=0,
                        font=("Roboto", 14))

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

        # Arama Kutusu (Anlık Arama)
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.load_cars())

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            textvariable=self.search_var,
            placeholder_text="Plaka, Marka veya Model ara...",
            width=450,
            height=45,
            corner_radius=10,
            font=("Roboto", 14)
        )
        self.search_entry.pack(side="left", padx=20, pady=15)

        # Durum Filtresi Etiketi ve Menüsü
        ctk.CTkLabel(self.search_frame, text="Durum Filtresi:", font=("Roboto", 14, "bold")).pack(side="left",
                                                                                                  padx=(10, 5))

        self.filter_var = ctk.StringVar(value="tümü")
        self.filter_menu = ctk.CTkOptionMenu(
            self.search_frame,
            variable=self.filter_var,
            values=["Tümü", "Müsait", "Kirada"],
            command=lambda x: self.load_cars(),
            width=150,
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

        # SOL GRUP: Veri Yönetimi
        self.add_btn = ctk.CTkButton(self.button_frame, text=" Araç Ekle", command=self.open_add_car_window,
                                     fg_color="#2ecc71", hover_color="#27ae60", font=btn_font, height=45)
        self.add_btn.pack(side="left", padx=5)

        self.edit_btn = ctk.CTkButton(self.button_frame, text="Düzenle", command=self.open_edit_car_window,
                                      fg_color="#f39c12", hover_color="#e67e22", font=btn_font, height=45)
        self.edit_btn.pack(side="left", padx=5)

        self.delete_btn = ctk.CTkButton(self.button_frame, text="Sil", command=self.delete_selected_car,
                                        fg_color="#e74c3c", hover_color="#c0392b", font=btn_font, height=45)
        self.delete_btn.pack(side="left", padx=5)

        # SAĞ GRUP: Kiralama ve Analiz
        # İstatistik Butonu (Yeni)
        self.stats_btn = ctk.CTkButton(self.button_frame, text=" İstatistikler", command=self.open_stats_window,
                                       fg_color="#1abc9c", hover_color="#16a085", font=btn_font, height=45)
        self.stats_btn.pack(side="right", padx=5)

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

        # İlk açılışta verileri yükle
        self.load_cars()

    def create_table(self):
        # Kaydırma Çubuğu
        self.scrollbar = ctk.CTkScrollbar(self.table_frame)
        self.scrollbar.pack(side="right", fill="y", padx=2, pady=2)

        self.tree = ttk.Treeview(
            self.table_frame,
            columns=("plaka", "marka", "model", "ucret", "durum"),
            show="headings",
            yscrollcommand=self.scrollbar.set
        )
        self.scrollbar.configure(command=self.tree.yview)

        # Sütun Genişlikleri ve Başlıkları
        cols = {"plaka": ("Plaka", 150), "marka": ("Marka", 220), "model": ("Model", 220),
                "ucret": ("Günlük Ücret", 160), "durum": ("Durum", 160)}

        for col, (text, width) in cols.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="center")

        # Durum Renkleri
        self.tree.tag_configure("müsait", foreground="#2ecc71")  # Yeşil
        self.tree.tag_configure("kirada", foreground="#e74c3c")  # Kırmızı

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    def load_cars(self):
        self.tree.delete(*self.tree.get_children())
        search_query = self.search_var.get().lower().strip()
        filter_status = self.filter_var.get()

        for car in get_all_cars():
            # Arama Kontrolü
            match_search = any(search_query in str(car[k]).lower() for k in ["plaka", "marka", "model"])
            if search_query and not match_search:
                continue

            # Filtre Kontrolü
            if filter_status != "tümü" and car["durum"] != filter_status:
                continue

            tag = "müsait" if car["durum"] == "müsait" else "kirada"
            self.tree.insert("", "end", values=(
                car["plaka"], car["marka"], car["model"], f"{car['ucret']} ₺", car["durum"].capitalize()
            ), tags=(tag,))

    def refresh_table(self):
        self.load_cars()

    # --- AKSİYONLAR ---

    def open_stats_window(self):
        StatsWindow(self.root)

    def open_add_car_window(self):
        AddCarWindow(self.root, self.refresh_table)

    def open_edit_car_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Seçim Yapın", "Lütfen düzenlemek istediğiniz aracı seçin.")
            return
        plaka = self.tree.item(selected[0])["values"][0]
        for car in get_all_cars():
            if car["plaka"] == plaka:
                EditCarWindow(self.root, car, self.refresh_table)
                break

    def delete_selected_car(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Seçim Yapın", "Lütfen silmek istediğiniz aracı seçin.")
            return
        plaka = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Silme Onayı", f"{plaka} plakalı araç kalıcı olarak silinecek. Onaylıyor musunuz?"):
            delete_car(plaka)
            self.load_cars()

    def open_rent_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Seçim Yapın", "Lütfen kiralamak istediğiniz aracı seçin.")
            return
        values = self.tree.item(selected[0])["values"]
        plaka, ucret = values[0], int(values[3].replace(" ₺", ""))

        # Müsaitlik kontrolü
        for car in get_all_cars():
            if car["plaka"] == plaka and car["durum"] != "müsait":
                messagebox.showerror("Hata", "Bu araç şu an başka bir müşteride!")
                return
        RentWindow(self.root, plaka, ucret, self.refresh_table)

    def return_car(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Seçim Yapın", "Lütfen iade edilecek aracı seçin.")
            return
        plaka = self.tree.item(selected[0])["values"][0]
        if return_car_by_plate(plaka):
            messagebox.showinfo("Başarılı", "Araç teslim alındı ve müsait duruma getirildi.")
            self.load_cars()
        else:
            messagebox.showwarning("Uyarı", "Bu araç zaten müsait.")