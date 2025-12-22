import customtkinter as ctk
from gui.main_window import MainWindow

#renk modları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk() #tk.Tk yerine custom olduğu için ctk.CTk

root.geometry("1280x720")
root.title("Araç Kiralama Otomasyonu")

app = MainWindow(root)
root.mainloop()