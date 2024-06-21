import customtkinter as ctk
from app.main_window import MainWindow
from logging_config import LOGGING_CONFIG
import logging.config

# Apply logging configuration
logging.config.dictConfig(LOGGING_CONFIG)

if __name__ == "__main__":
    from app.styles import apply_styles

    apply_styles()
    ctk.set_appearance_mode("Light")  # Set to light mode
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("Cisco Macro Uploader")

    main_window = MainWindow(app)
    main_window.pack(expand=True, fill="both")

    app.mainloop()
