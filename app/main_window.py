import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from app.utils.csv_utils import validate_csv, process_csv
from app.utils.template_utils import download_template
from PIL import Image
import logging

class MainWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.logger = logging.getLogger('main')

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

        self.upload_button = ctk.CTkButton(self.button_frame, text="Upload CSV", command=self.start_upload_thread, fg_color="#007BFF", hover_color="#0056b3", border_width=1, corner_radius=5)
        self.upload_button.grid(row=0, column=2, padx=10, pady=10)

        self.download_log_button = ctk.CTkButton(self.button_frame, text="Download Log File", command=self.download_log, fg_color="#007BFF", hover_color="#0056b3", border_width=1, corner_radius=5)
        self.download_log_button.grid(row=0, column=3, padx=10, pady=10)

        # Scrolling Text Box
        self.log_text = ctk.CTkTextbox(self, width=600, height=200, wrap="word")
        self.log_text.pack(pady=10)

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

    def start_upload_thread(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.upload_thread = threading.Thread(target=self.upload_csv, args=(file_path,))
            self.upload_thread.start()

    def upload_csv(self, file_path):
        try:
            # Clear log text box
            self.log_text.delete(1.0, "end")
            self.log_text.insert("end", "Starting upload...\n")
            self.update_idletasks()

            success, failures = process_csv(file_path, self.update_progress)
            if failures:
                self.show_message("warning", "Upload Completed with Errors", f"CSV file processed with some failures. See log for details.")
            else:
                self.show_message("info", "Success", "CSV file processed and macros uploaded successfully!")

            self.log_text.insert("end", "Upload completed.\n")
            self.update_idletasks()
        except ValueError as e:
            error_message = f"CSV validation errors:\n\n• {str(e).replace('\n', '\n• ')}"
            self.show_message("error", "Error", error_message)
        except PermissionError as e:
            self.show_message("error", "Permission Error", f"Error: {e}")
        except TimeoutError as e:
            self.show_message("error", "Timeout Error", f"Error: {e}")
        except ConnectionError as e:
            self.show_message("error", "Connection Error", f"Error: {e}")
        except Exception as e:
            self.show_message("error", "Error", f"Error processing file: {e}")

    def show_message(self, message_type, title, message):
        if message_type == "info":
            messagebox.showinfo(title, message)
        elif message_type == "warning":
            messagebox.showwarning(title, message)
        elif message_type == "error":
            messagebox.showerror(title, message)

    def update_progress(self, message, failed=False):
        self.log_text.insert("end", f"{message}\n")
        if failed:
            self.log_text.tag_add("failed", "end-2c", "end-1c")
            self.log_text.tag_config("failed", foreground="red")
        self.log_text.see("end")
        self.update_idletasks()

    def download_log(self):
        log_file_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'consolidated.log')
        if not os.path.exists(log_file_path):
            messagebox.showerror("Error", "Log file not found.")
            return
        
        with open(log_file_path, 'r') as log_file:
            log_data = log_file.read()

        save_path = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log Files", "*.log")], initialfile="consolidated.log")
        if save_path:
            try:
                with open(save_path, 'w') as output_file:
                    output_file.write(log_data)
                messagebox.showinfo("Download Success", f"Log file downloaded successfully to {save_path}!")
            except Exception as e:
                messagebox.showerror("Error", f"Error downloading log file: {e}")

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
