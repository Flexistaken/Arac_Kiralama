import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
from services.car_service import get_all_cars
from services.rental_service import load_rentals


class StatsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("İstatistikler ve Gelir Analizi")
        self.geometry("950x750")
        self.attributes("-topmost", True)

        # Verileri Yükle
        rentals = load_rentals()
        cars = get_all_cars()

        # --- 1. HESAPLAMALAR ---

        # A. Toplam Gelir
        total_income = sum(r.get("toplam_ucret", 0) for r in rentals)

        # B. Kirada Olan Araç Sayısı
        rented_count = len([c for c in cars if c["durum"] == "kirada"])

        # C. En Çok Kiralanan Marka Hesaplama
        # Önce plakaları markalarla eşleştiren bir sözlük (dictionary) oluşturalım
        plate_to_brand = {c["plaka"]: c["marka"] for c in cars}

        # Kiralama geçmişindeki her bir işlem için markayı bulup sayalım
        rented_brands = []
        for r in rentals:
            plaka = r.get("plaka")
            brand = plate_to_brand.get(plaka, "Bilinmeyen")
            rented_brands.append(brand)

        brand_counts = Counter(rented_brands)
        # En çok tekrar eden markayı alalım
        most_rented_brand = brand_counts.most_common(1)[0][0] if brand_counts else "-"

        # --- 2. ARAYÜZ (Görsel Kartlar) ---
        self.card_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.card_frame.pack(pady=30, padx=20, fill="x")

        self.create_card("Toplam Ciro", f"{total_income} ₺", "#2ecc71").pack(side="left", expand=True, padx=10)
        self.create_card("Aktif Kiralamalar", str(rented_count), "#3498db").pack(side="left", expand=True, padx=10)
        self.create_card("En Çok Kiralanan Marka", most_rented_brand, "#f1c40f").pack(side="left", expand=True, padx=10)

        # --- 3. GRAFİK ALANI (Matplotlib) ---
        self.graph_container = ctk.CTkFrame(self, corner_radius=15)
        self.graph_container.pack(pady=10, padx=20, fill="both", expand=True)

        self.draw_graph(rentals)

    def create_card(self, title, value, color):
        card = ctk.CTkFrame(self.card_frame, corner_radius=15, border_width=2, border_color=color)
        ctk.CTkLabel(card, text=title, font=("Roboto", 15, "bold")).pack(pady=(15, 0), padx=25)
        ctk.CTkLabel(card, text=value, font=("Roboto", 28, "bold"), text_color=color).pack(pady=(5, 15), padx=25)
        return card

    def draw_graph(self, rentals):
        # Aylık Gelir Gruplama (YYYY-MM formatında)
        monthly_income = {}
        for r in rentals:
            # Tarih formatının YYYY-MM-DD olduğunu varsayarak ilk 7 karakteri alıyoruz
            month = r["baslangic"][:7]
            monthly_income[month] = monthly_income.get(month, 0) + r.get("toplam_ucret", 0)

        # Grafiğin düzgün görünmesi için ayları sıralayalım
        sorted_months = sorted(monthly_income.keys())
        values = [monthly_income[m] for m in sorted_months]

        # Matplotlib Figürü
        fig = Figure(figsize=(6, 4), dpi=100, facecolor='#2b2b2b')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2b2b2b')

        # Çizgi Grafiği Ayarları
        ax.plot(sorted_months, values, marker='o', color='#1abc9c', linewidth=3, markersize=8)
        ax.fill_between(sorted_months, values, color='#1abc9c', alpha=0.2)

        # Eksenleri Beyaz Yapma (Karanlık Mod İçin)
        ax.tick_params(colors='white', labelsize=10)
        for spine in ax.spines.values():
            spine.set_color('white')

        ax.set_title("Aylık Gelir Grafiği (₺)", color='white', fontsize=16, pad=20)
        ax.grid(True, linestyle='--', alpha=0.3, color='gray')

        # Tkinter içine gömme işlemi
        canvas = FigureCanvasTkAgg(fig, master=self.graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)