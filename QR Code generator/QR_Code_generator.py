import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
import os
import requests
from pathlib import Path

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Stile
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10))
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        
        # Inizializza le variabili di istanza
        self.qr_image = None
        self.logo_path = None
        self.valid_colors = [
            "black", "white", "red", "blue", "green", "yellow", 
            "cyan", "magenta", "gray"
        ]
        self.valid_formats = ["PNG", "JPEG", "JPG", "BMP", "GIF"]
        
        # Crea i widget
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titolo
        header = ttk.Label(
            main_frame, 
            text="QR Code Generator", 
            style='Header.TLabel'
        )
        header.pack(pady=(0, 20))
        
        # Frame per input
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        # URL Input
        ttk.Label(input_frame, text="URL:").pack(anchor='w')
        self.url_entry = ttk.Entry(input_frame, width=50)
        self.url_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Frame per le opzioni
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        # Colori
        colors_frame = ttk.Frame(options_frame)
        colors_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(colors_frame, text="Fill Color:").pack(side=tk.LEFT)
        self.fill_color = ttk.Combobox(
            colors_frame, 
            values=self.valid_colors, 
            width=15
        )
        self.fill_color.set("black")
        self.fill_color.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(colors_frame, text="Background:").pack(side=tk.LEFT, padx=(10, 0))
        self.back_color = ttk.Combobox(
            colors_frame, 
            values=self.valid_colors, 
            width=15
        )
        self.back_color.set("white")
        self.back_color.pack(side=tk.LEFT, padx=5)
        
        # Box size
        size_frame = ttk.Frame(options_frame)
        size_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(size_frame, text="Box Size:").pack(side=tk.LEFT)
        self.box_size = ttk.Spinbox(
            size_frame, 
            from_=1, 
            to=20, 
            width=5
        )
        self.box_size.set(10)
        self.box_size.pack(side=tk.LEFT, padx=5)
        
        # Format selection
        ttk.Label(size_frame, text="Format:").pack(side=tk.LEFT, padx=(10, 0))
        self.format_combo = ttk.Combobox(
            size_frame, 
            values=self.valid_formats, 
            width=10
        )
        self.format_combo.set("PNG")
        self.format_combo.pack(side=tk.LEFT, padx=5)
        
        # Logo options
        logo_frame = ttk.Frame(options_frame)
        logo_frame.pack(fill=tk.X, pady=5)
        
        self.use_logo_var = tk.BooleanVar()
        self.use_logo_check = ttk.Checkbutton(
            logo_frame, 
            text="Add Logo", 
            variable=self.use_logo_var,
            command=self.toggle_logo_button
        )
        self.use_logo_check.pack(side=tk.LEFT)
        
        self.logo_button = ttk.Button(
            logo_frame, 
            text="Select Logo", 
            command=self.select_logo,
            state=tk.DISABLED
        )
        self.logo_button.pack(side=tk.LEFT, padx=5)
        
        # Preview frame
        self.preview_frame = ttk.Frame(main_frame)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Preview label
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.pack(expand=True)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            buttons_frame, 
            text="Generate Preview", 
            command=self.generate_preview
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame, 
            text="Save QR Code", 
            command=self.save_qr_code
        ).pack(side=tk.LEFT, padx=5)
    
    def is_valid_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        try:
            response = requests.get(url)
            return response.status_code == 200, url
        except:
            return False, url
    
    def toggle_logo_button(self):
        if self.use_logo_var.get():
            self.logo_button.configure(state=tk.NORMAL)
        else:
            self.logo_button.configure(state=tk.DISABLED)
            self.logo_path = None
    
    def select_logo(self):
        logo_file = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        if logo_file:
            self.logo_path = logo_file
    
    def generate_qr_code(self):
        url = self.url_entry.get().strip()
        valid, url = self.is_valid_url(url)
        
        if not valid:
            messagebox.showerror("Error", "Invalid URL!")
            return None
        
        try:
            qr = qrcode.QRCode(
                box_size=int(self.box_size.get()),
                border=4
            )
            qr.add_data(url)
            image = qr.make_image(
                fill_color=self.fill_color.get(),
                back_color=self.back_color.get()
            ).convert("RGB")
            
            if self.use_logo_var.get() and self.logo_path:
                # Add logo to QR code
                logo = Image.open(self.logo_path)
                qr_width, qr_height = image.size
                logo_size = int(qr_width * 0.15)
                logo = logo.convert("RGBA")
                logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
                logo_alpha = logo.split()[3]
                
                x_offset = (qr_width - logo_size) // 2
                y_offset = (qr_height - logo_size) // 2
                image.paste(logo, (x_offset, y_offset), mask=logo_alpha)
            
            return image
        except Exception as e:
            messagebox.showerror("Error", f"Error generating QR code: {str(e)}")
            return None
    
    def generate_preview(self):
        image = self.generate_qr_code()
        if image:
            # Resize for preview while maintaining aspect ratio
            preview_size = (300, 300)
            image.thumbnail(preview_size, Image.LANCZOS)
            
            # Convert to PhotoImage for display
            photo = ImageTk.PhotoImage(image)
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo  # Keep a reference
            
            self.qr_image = image  # Save for later use
    
    def save_qr_code(self):
        if not self.qr_image:
            messagebox.showwarning("Warning", "Generate a QR code first!")
            return
        
        # Ask for save location
        file_format = self.format_combo.get()
        file_types = [(f"{file_format} files", f"*.{file_format.lower()}")]
        save_path = filedialog.asksaveasfilename(
            defaultextension=f".{file_format.lower()}",
            filetypes=file_types
        )
        
        if save_path:
            try:
                self.qr_image.save(save_path, format=file_format)
                messagebox.showinfo(
                    "Success", 
                    f"QR code saved successfully as {Path(save_path).name}!"
                )
            except Exception as e:
                messagebox.showerror(
                    "Error", 
                    f"Error saving QR code: {str(e)}"
                )

def main():
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()