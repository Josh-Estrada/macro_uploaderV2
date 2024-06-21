import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from app.utils import validate_csv, process_csv, download_template
from PIL import Image

class MainWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Cisco Macro Uploader", font=("Arial", 24, "bold"), bg_color="transparent")
        self.title_label.pack(pady=20)

        # Description
        self.description_label = ctk.CTkLabel(self, text="This tool allows you to upload the same Cisco macro to multiple Cisco endpoints in bulk or unique Cisco macros to multiple Cisco endpoints in bulk. Download the CSV template, fill in the required values, validate the file, and upload it to get started. Ensure the CSV columns are named exactly as 'ip_address', 'username', 'password', and 'macro_file_path'. No rows should be blank.", wraplength=600, bg_color="transparent")
        self.description_label.pack(pady=20, padx=20)

        # Button Frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)

        # Buttons
        self.download_button = ctk.CTkButton(self.button_frame, text="Download CSV Template", command=self.download_template, fg_color="#007BFF", hover_color="#0056b3", border_width=1, corner_radius=5)
        self.download_button.grid(row=0, column=0, padx=10, pady=10)

        self.validate_button = ctk.CTkButton(self.button_frame, text="Validate CSV", command=self.validate_csv, fg_color="#007BFF", hover_color="#0056b3", border_width=1, corner_radius=5)
        self.validate_button.grid(row=0, column=1, padx=10, pady=10)

        self.upload_button = ctk.CTkButton(self.button_frame, text="Upload CSV", command=self.upload_csv, fg_color="#007BFF", hover_color="#0056b3", border_width=1, corner_radius=5)
        self.upload_button.grid(row=0, column=2, padx=10, pady=10)

        # Load and place the logo image
        self.logo_image_path = os.path.join(os.path.dirname(__file__), 'resources', 'logo.png')
        self.load_logo_image()
        self.logo_label = ctk.CTkLabel(self, image=self.logo_photo, bg_color="transparent", text="")
        self.logo_label.pack(pady=20)

    def load_logo_image(self):
        self.logo_image = Image.open(self.logo_image_path)
        self.logo_image = self.logo_image.resize((675, 450), Image.Resampling.LANCZOS)
        self.logo_photo = ctk.CTkImage(light_image=self.logo_image, dark_image=self.logo_image, size=(675, 450))

    def download_template(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], initialfile="template.csv")
        if save_path:
            try:
                download_template(save_path)
                messagebox.showinfo("Download Success", f"CSV template downloaded successfully to {save_path}!")
            except Exception as e:
                messagebox.showerror("Error", f"Error downloading template: {e}")

    def validate_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                errors = validate_csv(file_path)
                if errors:
                    error_message = f"CSV validation errors:\n\n• {str('\n• '.join(errors))}"
                    messagebox.showerror("Validation Error", error_message)
                else:
                    messagebox.showinfo("Validation Success", "CSV file is valid!")
            except Exception as e:
                messagebox.showerror("Error", f"Error validating file: {e}")

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                process_csv(file_path)
                messagebox.showinfo("Success", "CSV file processed successfully!")
            except ValueError as e:
                error_message = f"CSV validation errors:\n\n• {str(e).replace('\n', '\n• ')}"
                messagebox.showerror("Error", error_message)
            except Exception as e:
                messagebox.showerror("Error", f"Error processing file: {e}")

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
