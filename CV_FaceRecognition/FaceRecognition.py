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

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Face Recognition")
        self.root.geometry("800x600")
        
        # Inizializza il modello InsightFace
        self.app = FaceAnalysis(name='buffalo_l')
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        
        self.known_embeddings = {}
        self.load_data()
        
        self.setup_ui()
        self.setup_styles()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 12), padding=10)
        self.style.configure('TFrame', background='#2E2E2E')
        self.root.configure(bg='#2E2E2E')

    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)

        title = tk.Label(main_frame, 
                       text="Advanced Face ID System",
                       font=('Arial', 24, 'bold'),
                       fg='#00FFAA',
                       bg='#2E2E2E')
        title.pack(pady=30)

        btn_style = {'style': 'TButton', 'width': 25}
        ttk.Button(main_frame, 
                 text="Register New User", 
                 command=self.register_user, **btn_style).pack(pady=15)
        
        ttk.Button(main_frame,
                 text="Real-Time Recognition",
                 command=self.start_recognition, **btn_style).pack(pady=15)

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
                messagebox.showerror("Error", f"Each image must contain exactly one face\nProblem with: {os.path.basename(file_path)}")
                return
                
            embeddings.append(faces[0].embedding)

        # Calcola l'embedding medio dai 3 campioni
        avg_embedding = np.mean(embeddings, axis=0)
        self.known_embeddings[name] = avg_embedding
        self.save_data()
        messagebox.showinfo("Success", "User registered successfully!")

    def start_recognition(self):
        recognition_window = tk.Toplevel(self.root)
        recognition_window.title("Face Recognition Live")
        
        video_panel = tk.Label(recognition_window)
        video_panel.pack()

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.stop_event = threading.Event()
        self.threshold = 0.6  # Soglia di similarità

        # Avvia il thread per la webcam
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
                # Rilevamento facce
                faces = self.app.get(frame)
                
                for face in faces:
                    x1, y1, x2, y2 = face.bbox.astype(int)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Calcolo similarità
                    max_similarity = 0
                    identity = "Sconosciuto"
                    for name, saved_embedding in self.known_embeddings.items():
                        similarity = cosine_similarity([face.embedding], [saved_embedding])[0][0]
                        if similarity > max_similarity and similarity > self.threshold:
                            max_similarity = similarity
                            identity = name
                    
                    # Disegna risultato
                    color = (0, 255, 0) if identity != "Sconosciuto" else (0, 0, 255)
                    cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), color, cv2.FILLED)
                    cv2.putText(frame, f"{identity} ({max_similarity:.2f})", (x1 + 6, y2 - 6), 
                               cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

                # Converti per Tkinter
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                video_panel.imgtk = imgtk
                video_panel.configure(image=imgtk)
            
            # Riduci il carico sulla CPU
            self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()