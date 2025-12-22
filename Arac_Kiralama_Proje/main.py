import customtkinter as ctk
from gui.main_window import MainWindow

# --- UYGULAMA GENELİ GÖRÜNÜM AYARLARI ---
# Bu ayarlar tüm alt pencerelerde (Ekle, Düzenle, İstatistik vb.) otomatik geçerli olur.
ctk.set_appearance_mode("dark")  # "dark" (Karanlık), "light" (Aydınlık) veya "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue" temalarından birini seçebilirsin


def main():
    # 1. Ana uygulama nesnesini oluştur (Standard tk.Tk yerine ctk.CTk)
    root = ctk.CTk()

    # 2. Başlangıç pencere boyutunu ayarla
    # MainWindow içinde de ayarlanabilir ama burada temel bir değer vermek iyidir.
    root.geometry("1280x720")
    root.title("Araç Kiralama Otomasyonu")

    # 3. MainWindow sınıfını başlat
    # root nesnesini MainWindow'a gönderiyoruz
    app = MainWindow(root)

    # 4. Uygulamanın çalışır kalmasını sağlayan ana döngü
    root.mainloop()


if __name__ == "__main__":
    # Script doğrudan çalıştırıldığında main() fonksiyonunu çağır
    main()