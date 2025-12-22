import customtkinter as ctk
from gui.main_window import MainWindow

# 1. Uygulama Geneli Görünüm Ayarları
ctk.set_appearance_mode("dark")  # "dark", "light" veya "system" (OS ayarına göre)
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


def main():
    # 2. Ana Pencere Oluşturma (tk.Tk yerine ctk.CTk)
    root = ctk.CTk()

    # Pencere simgesi (Eğer varsa .ico dosyanı buraya ekleyebilirsin)
    # root.iconbitmap("assets/icon.ico")

    # 3. Uygulamayı Başlat
    app = MainWindow(root)

    # 4. Ana Döngü
    root.mainloop()


if __name__ == "__main__":
    main()