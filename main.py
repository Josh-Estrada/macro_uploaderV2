import customtkinter as ctk
from app.main_window import MainWindow
from app.styles import apply_styles

if __name__ == "__main__":
    apply_styles()
    ctk.set_appearance_mode("Light")  # Set to light mode
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("Cisco Macro Uploader")

    main_window = MainWindow(app)
    main_window.pack(expand=True, fill="both")

    app.mainloop()
