import customtkinter as ctk
from gui.main_window import MainWindow

# 1. Uygulama Geneli Görünüm Ayarları
ctk.set_appearance_mode("dark")  # "dark", "light" veya "system" (OS ayarına göre)
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

root = ctk.CTk()
app = MainWindow(root)
root.mainloop()