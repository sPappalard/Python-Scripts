import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
import pickle
import insightface
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity
import threading

# Colori e stile moderni
BG_COLOR = "#2b2b2b"           # sfondo scuro
ACCENT_COLOR = "#1abc9c"       # colore di accento (verde chiaro)
TEXT_COLOR = "#ecf0f1"         # testo bianco
BUTTON_BG = "#34495e"
BUTTON_FG = "#ecf0f1"
FONT_FAMILY = "Helvetica"

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Face Recognition")
        self.root.geometry("900x650")
        self.root.configure(bg=BG_COLOR)
        
        # Inizializza il modello InsightFace
        self.app = FaceAnalysis(name='buffalo_l')
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        
        self.known_embeddings = {}
        self.load_data()
        
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        self.style = ttk.Style()
        # Usa un tema nativo e personalizza le opzioni
        self.style.theme_use('clam')
        self.style.configure("TFrame", background=BG_COLOR)
        self.style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=(FONT_FAMILY, 12))
        self.style.configure("Header.TLabel", font=(FONT_FAMILY, 24, "bold"), foreground=ACCENT_COLOR, background=BG_COLOR)
        self.style.configure("TButton", font=(FONT_FAMILY, 12), padding=10, relief="flat", background=BUTTON_BG, foreground=BUTTON_FG)
        self.style.map("TButton",
                       background=[("active", ACCENT_COLOR)],
                       foreground=[("active", BG_COLOR)])
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        header = ttk.Label(main_frame, text="Advanced Face ID System", style="Header.TLabel")
        header.pack(pady=(0, 30))
        
        btn_style = {"width": 30}
        ttk.Button(main_frame, text="Register New User", command=self.register_user, **btn_style).pack(pady=10)
        ttk.Button(main_frame, text="Real-Time Recognition", command=self.start_recognition, **btn_style).pack(pady=10)
        ttk.Button(main_frame, text="Non Real-Time Recognition", command=self.non_real_time_recognition, **btn_style).pack(pady=10)
        ttk.Button(main_frame, text="Manage Registered Users", command=self.manage_users, **btn_style).pack(pady=10)

    def load_data(self):
        if os.path.exists('embeddings.pkl'):
            with open('embeddings.pkl', 'rb') as f:
                self.known_embeddings = pickle.load(f)

    def save_data(self):
        with open('embeddings.pkl', 'wb') as f:
            pickle.dump(self.known_embeddings, f)

    def register_user(self):
        files = filedialog.askopenfilenames(title="Select 3 Face Images",
                                            filetypes=(("Image files", "*.jpg *.jpeg *.png"),))
        if len(files) != 3:
            messagebox.showerror("Error", "Please select exactly 3 images")
            return

        name = simpledialog.askstring("Input", "Enter user name:")
        if not name:
            return

        embeddings = []
        for file_path in files:
            img = cv2.imread(file_path)
            faces = self.app.get(img)
            if len(faces) != 1:
                messagebox.showerror("Error", f"Each image must contain exactly one face.\nIssue with: {os.path.basename(file_path)}")
                return
            embeddings.append(faces[0].embedding)

        avg_embedding = np.mean(embeddings, axis=0)
        self.known_embeddings[name] = avg_embedding
        self.save_data()
        self.update_registered_list()
        messagebox.showinfo("Success", "User registered successfully!")

    def start_recognition(self):
        recognition_window = tk.Toplevel(self.root)
        recognition_window.title("Face Recognition Live")
        recognition_window.configure(bg=BG_COLOR)
        
        video_panel = tk.Label(recognition_window, bg=BG_COLOR)
        video_panel.pack(padx=10, pady=10)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.stop_event = threading.Event()
        self.threshold = 0.6  # similarità

        self.thread = threading.Thread(target=self.process_frame, args=(video_panel,))
        self.thread.daemon = True
        self.thread.start()

        def on_close():
            self.stop_event.set()
            self.cap.release()
            recognition_window.destroy()

        recognition_window.protocol("WM_DELETE_WINDOW", on_close)

    def process_frame(self, video_panel):
        while not self.stop_event.is_set():
            ret, frame = self.cap.read()
            if ret:
                faces = self.app.get(frame)
                for face in faces:
                    x1, y1, x2, y2 = face.bbox.astype(int)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    max_similarity = 0
                    identity = "Unknown"
                    for name, saved_embedding in self.known_embeddings.items():
                        similarity = cosine_similarity([face.embedding], [saved_embedding])[0][0]
                        if similarity > max_similarity and similarity > self.threshold:
                            max_similarity = similarity
                            identity = name
                    color = (0, 255, 0) if identity != "Unknown" else (0, 0, 255)
                    cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), color, cv2.FILLED)
                    cv2.putText(frame, f"{identity} ({max_similarity:.2f})", (x1 + 6, y2 - 6),
                                cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img_rgb)
                imgtk = ImageTk.PhotoImage(image=img_pil)
                video_panel.imgtk = imgtk
                video_panel.configure(image=imgtk)
            self.root.update()

    def non_real_time_recognition(self):
        nrt_window = tk.Toplevel(self.root)
        nrt_window.title("Non Real-Time Face Recognition")
        nrt_window.geometry("900x600")
        nrt_window.configure(bg=BG_COLOR)

        main_frame = ttk.Frame(nrt_window)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)

        lbl_title = ttk.Label(left_frame, text="Upload an Image to Verify", font=(FONT_FAMILY, 14))
        lbl_title.pack(pady=10)

        self.nrt_image_path = None
        self.nrt_image = None

        self.nrt_image_label = tk.Label(left_frame, text="No image loaded", bg=BG_COLOR, fg=TEXT_COLOR)
        self.nrt_image_label.pack(pady=10)

        ttk.Button(left_frame, text="Load Image", command=self.load_nrt_image).pack(pady=10)
        ttk.Button(left_frame, text="Verify", command=self.verify_nrt_image).pack(pady=10)

        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        lbl_registered = ttk.Label(right_frame, text="Registered Users", font=(FONT_FAMILY, 14))
        lbl_registered.pack(pady=10)

        self.registered_listbox = tk.Listbox(right_frame, font=(FONT_FAMILY, 12), bg=BUTTON_BG, fg=TEXT_COLOR, selectbackground=ACCENT_COLOR)
        self.registered_listbox.pack(expand=True, fill="both", padx=10, pady=10)
        self.update_registered_list()

    def load_nrt_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image",
                                               filetypes=(("Image files", "*.jpg *.jpeg *.png"),))
        if file_path:
            self.nrt_image_path = file_path
            img = cv2.imread(file_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img)
            img_pil.thumbnail((300, 300))
            self.nrt_image = ImageTk.PhotoImage(img_pil)
            self.nrt_image_label.configure(image=self.nrt_image, text="")

    def update_registered_list(self):
        if hasattr(self, 'registered_listbox'):
            self.registered_listbox.delete(0, tk.END)
            if not self.known_embeddings:
                self.registered_listbox.insert(tk.END, "No registered user")
            else:
                for name in self.known_embeddings.keys():
                    self.registered_listbox.insert(tk.END, name)

    def verify_nrt_image(self):
        if not self.nrt_image_path:
            messagebox.showerror("Error", "Load an image first")
            return

        img = cv2.imread(self.nrt_image_path)
        if img is None:
            messagebox.showerror("Error", "Cannot open image")
            return

        faces = self.app.get(img)
        if len(faces) == 0:
            messagebox.showerror("Error", "No face detected in the image")
            return

        threshold = 0.6
        recognized_faces = []
        for face in faces:
            max_similarity = 0
            identity = None
            for name, saved_embedding in self.known_embeddings.items():
                similarity = cosine_similarity([face.embedding], [saved_embedding])[0][0]
                if similarity > max_similarity and similarity > threshold:
                    max_similarity = similarity
                    identity = name
            if identity:
                recognized_faces.append((face, identity, max_similarity))

        if recognized_faces:
            zoomed_faces = []
            for face, identity, sim in recognized_faces:
                x1, y1, x2, y2 = face.bbox.astype(int)
                h, w, _ = img.shape
                margin = 20
                x1m = max(x1 - margin, 0)
                y1m = max(y1 - margin, 0)
                x2m = min(x2 + margin, w)
                y2m = min(y2 + margin, h)
                crop = img[y1m:y2m, x1m:x2m].copy()
                cv2.rectangle(crop, (0, 0), (crop.shape[1]-1, crop.shape[0]-1), (0, 255, 0), 3)
                cv2.putText(crop, identity, (5, crop.shape[0]-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                zoom = cv2.resize(crop, (300, 300))
                zoomed_faces.append(zoom)
            if len(zoomed_faces) > 1:
                combined = np.hstack(zoomed_faces)
            else:
                combined = zoomed_faces[0]
            combined_rgb = cv2.cvtColor(combined, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(combined_rgb)
            self.nrt_image = ImageTk.PhotoImage(pil_img)
            self.nrt_image_label.configure(image=self.nrt_image)
            
            recognized_names = ', '.join([identity for (_, identity, _) in recognized_faces])
            messagebox.showinfo("Result", f"Recognized: {recognized_names}")
        else:
            annotated_image = img.copy()
            for face in faces:
                x1, y1, x2, y2 = face.bbox.astype(int)
                cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(annotated_image)
            pil_img.thumbnail((300, 300))
            self.nrt_image = ImageTk.PhotoImage(pil_img)
            self.nrt_image_label.configure(image=self.nrt_image)
            messagebox.showinfo("Result", "No registered face detected among those found")

    def manage_users(self):
        manage_window = tk.Toplevel(self.root)
        manage_window.title("Manage Registered Users")
        manage_window.geometry("400x400")
        manage_window.configure(bg=BG_COLOR)
        
        lbl = ttk.Label(manage_window, text="Registered Users", font=(FONT_FAMILY, 14))
        lbl.pack(pady=10)
        
        listbox = tk.Listbox(manage_window, selectmode=tk.MULTIPLE, font=(FONT_FAMILY, 12), bg=BUTTON_BG, fg=TEXT_COLOR, selectbackground=ACCENT_COLOR)
        listbox.pack(expand=True, fill="both", padx=10, pady=10)
        
        for name in self.known_embeddings.keys():
            listbox.insert(tk.END, name)
        
        def delete_selected():
            selected_indices = listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("Warning", "Select at least one user to delete")
                return
            for index in reversed(selected_indices):
                name = listbox.get(index)
                if name in self.known_embeddings:
                    del self.known_embeddings[name]
                    listbox.delete(index)
            self.save_data()
            self.update_registered_list()
            messagebox.showinfo("Success", "Selected users have been deleted!")
        
        ttk.Button(manage_window, text="Delete Selected Users", command=delete_selected).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()