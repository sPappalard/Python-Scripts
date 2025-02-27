import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import whisper
import subprocess
import os
import tempfile
import threading
import time

# Estensioni video riconosciute
VIDEO_EXTENSIONS = [".mp4", ".avi", ".mov", ".mkv", ".flv"]

# Formati sottotitoli supportati
SUBTITLE_FORMATS = {
    "SubRip (.srt)": ".srt",
    "WebVTT (.vtt)": ".vtt",
    "Advanced SubStation Alpha (.ass)": ".ass"
}

def format_timestamp(seconds: float, format_type="srt") -> str:
    """Formatta il tempo in secondi nel formato specificato"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    
    if format_type == "srt" or format_type == "ass":
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
    elif format_type == "vtt":
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:03d}"
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

def save_subtitles(segments, output_path, format_type, log_func):
    """Genera e salva il file sottotitoli nel formato specificato"""
    try:
        file_ext = SUBTITLE_FORMATS[format_type]
        format_short = file_ext[1:]  # Rimuove il punto
        
        with open(output_path, "w", encoding="utf-8") as f:
            if format_short == "srt":
                for idx, seg in enumerate(segments, start=1):
                    start = format_timestamp(seg["start"], "srt")
                    end = format_timestamp(seg["end"], "srt")
                    text = seg["text"].strip()
                    f.write(f"{idx}\n{start} --> {end}\n{text}\n\n")
            
            elif format_short == "vtt":
                f.write("WEBVTT\n\n")
                for idx, seg in enumerate(segments, start=1):
                    start = format_timestamp(seg["start"], "vtt")
                    end = format_timestamp(seg["end"], "vtt")
                    text = seg["text"].strip()
                    f.write(f"{idx}\n{start} --> {end}\n{text}\n\n")
            
            elif format_short == "ass":
                f.write("[Script Info]\nScriptType: v4.00+\nPlayResX: 384\nPlayResY: 288\n\n")
                f.write("[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
                f.write("Style: Default,Arial,16,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n\n")
                f.write("[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
                
                for seg in segments:
                    start = format_timestamp(seg["start"], "ass")
                    end = format_timestamp(seg["end"], "ass")
                    text = seg["text"].strip()
                    f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")
        
        log_func(f"Sottotitoli salvati in: {output_path}")
    except Exception as e:
        log_func(f"Errore durante il salvataggio dei sottotitoli: {e}")

def extract_audio_from_video(video_path, output_audio_path, log_func):
    """
    Estrae l'audio dal video usando ffmpeg e lo salva nel percorso output_audio_path.
    """
    try:
        command = [
            "ffmpeg",
            "-y",  # sovrascrive se il file esiste
            "-i", video_path,
            "-vn",  # nessun video
            "-acodec", "pcm_s16le",  # codec audio per file wav
            "-ar", "16000",  # frequenza di campionamento 16kHz
            "-ac", "1",  # audio mono
            output_audio_path
        ]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        log_func(f"Audio estratto da: {video_path}")
    except subprocess.CalledProcessError as e:
        log_func(f"Errore durante l'estrazione audio: {e}")
        raise

def get_audio_duration(audio_path):
    """Ottiene la durata dell'audio in secondi usando ffprobe"""
    try:
        command = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError):
        return None

def transcribe_audio_with_progress(audio_path, model, log_func, progress_callback):
    """Trascrive l'audio tramite Whisper con aggiornamenti di progresso approssimativi"""
    log_func("Avvio della trascrizione...")
    
    # Ottieni la durata dell'audio
    duration = get_audio_duration(audio_path)
    if not duration:
        log_func("Impossibile determinare la durata dell'audio, il progresso sarà approssimativo.")
        # Imposta una durata di default
        duration = 600  # 10 minuti
    
    # Avvia thread separato per simulare il progresso
    def progress_updater():
        start_time = time.time()
        elapsed = 0
        while elapsed < duration * 1.2 and not progress_thread.cancelled:
            elapsed = time.time() - start_time
            progress = min(95, (elapsed / (duration * 1.1)) * 100)
            remaining = (duration * 1.1) - elapsed
            if remaining < 0:
                remaining = 0
                
            progress_msg = f"Progresso: {progress:.1f}% - Tempo rimanente stimato: {int(remaining//60)}m {int(remaining%60)}s"
            progress_callback(progress, progress_msg)
            time.sleep(1)
    
    progress_thread = threading.Thread(target=progress_updater)
    progress_thread.cancelled = False
    progress_thread.daemon = True
    progress_thread.start()
    
    try:
        # Esegui la trascrizione
        result = model.transcribe(audio_path, fp16=False)
        
        # Interrompi il thread di aggiornamento del progresso
        progress_thread.cancelled = True
        progress_thread.join(0.1)
        
        # Imposta progresso al 100% al completamento
        progress_callback(95, "Finalizzazione...")
        
        return result["segments"]
    except Exception as e:
        # Interrompi il thread di aggiornamento del progresso
        progress_thread.cancelled = True
        progress_thread.join(0.1)
        raise e

class SubtitleGeneratorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Generatore di Sottotitoli con Whisper")
        self.master.geometry("800x700")  # Dimensione iniziale della finestra
        self.model = None
        self.file_path = None
        self.output_path = None
        self.is_processing = False

        # Frame principale
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame per i controlli
        controls_frame = tk.LabelFrame(main_frame, text="Configurazione")
        controls_frame.pack(fill=tk.X, pady=5)

        # Frame per selezionare il file
        file_frame = tk.Frame(controls_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        self.select_button = tk.Button(file_frame, text="Seleziona File Audio/Video", command=self.select_file)
        self.select_button.pack(side=tk.LEFT, padx=5)
        
        self.file_label = tk.Label(file_frame, text="Nessun file selezionato")
        self.file_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Frame per selezionare la destinazione
        output_frame = tk.Frame(controls_frame)
        output_frame.pack(fill=tk.X, pady=5)
        
        self.output_button = tk.Button(output_frame, text="Seleziona Destinazione", command=self.select_output)
        self.output_button.pack(side=tk.LEFT, padx=5)
        
        self.output_label = tk.Label(output_frame, text="Nessuna destinazione selezionata")
        self.output_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Frame per selezionare il formato dei sottotitoli
        format_frame = tk.Frame(controls_frame)
        format_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(format_frame, text="Formato Sottotitoli:").pack(side=tk.LEFT, padx=5)
        
        self.format_var = tk.StringVar(value=list(SUBTITLE_FORMATS.keys())[0])
        format_menu = ttk.Combobox(format_frame, textvariable=self.format_var, values=list(SUBTITLE_FORMATS.keys()), state="readonly")
        format_menu.pack(side=tk.LEFT, padx=5)

        # Modello Whisper
        model_frame = tk.Frame(controls_frame)
        model_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(model_frame, text="Modello Whisper:").pack(side=tk.LEFT, padx=5)
        
        self.model_var = tk.StringVar(value="base")
        self.model_sizes = ["tiny", "base", "small", "medium", "large"]
        model_menu = ttk.Combobox(model_frame, textvariable=self.model_var, values=self.model_sizes, state="readonly")
        model_menu.pack(side=tk.LEFT, padx=5)
        
        # Nota sui modelli
        tk.Label(model_frame, text="(Modelli più grandi = più precisione, ma richiedono più tempo e memoria)").pack(side=tk.LEFT, padx=5)

        # Frame per il pulsante di avvio
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.generate_button = tk.Button(button_frame, text="Genera Sottotitoli", command=self.start_processing, state=tk.DISABLED)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = tk.Button(button_frame, text="Annulla", command=self.cancel_processing, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        # Barra di progresso
        progress_frame = tk.LabelFrame(main_frame, text="Progresso")
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5, padx=5)
        
        self.progress_label = tk.Label(progress_frame, text="In attesa...")
        self.progress_label.pack(pady=5)

        # Area log
        log_frame = tk.LabelFrame(main_frame, text="Log")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=80, height=20, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)

        # Caricamento del modello in un thread separato
        self.should_cancel = False
        self.log("Benvenuto nel Generatore di Sottotitoli con Whisper!")
        self.log("Seleziona un file audio o video per iniziare.")

    def log(self, message):
        """Aggiunge un messaggio all'area log"""
        self.log_text.config(state=tk.NORMAL)
        timestamp = time.strftime("[%H:%M:%S]", time.localtime())
        self.log_text.insert(tk.END, f"{timestamp} {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def select_file(self):
        """Apre il file dialog per selezionare un file audio o video"""
        filetypes = [("Audio/Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wav *.mp3"), ("All files", "*.*")]
        file_path = filedialog.askopenfilename(title="Seleziona file", filetypes=filetypes)
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.log(f"File selezionato: {file_path}")
            self.update_generate_button_state()

    def select_output(self):
        """Apre il file dialog per selezionare la destinazione di salvataggio"""
        format_name = self.format_var.get()
        extension = SUBTITLE_FORMATS[format_name]
        
        if self.file_path:
            # Usa il nome del file di input come suggerimento
            suggested_name = os.path.splitext(os.path.basename(self.file_path))[0] + extension
        else:
            suggested_name = "sottotitoli" + extension
        
        output_path = filedialog.asksaveasfilename(
            title="Salva sottotitoli come",
            defaultextension=extension,
            filetypes=[(format_name, f"*{extension}"), ("All files", "*.*")],
            initialfile=suggested_name
        )
        
        if output_path:
            self.output_path = output_path
            self.output_label.config(text=os.path.basename(output_path))
            self.log(f"Destinazione sottotitoli: {output_path}")
            self.update_generate_button_state()

    def update_generate_button_state(self):
        """Aggiorna lo stato del pulsante di generazione in base ai file selezionati"""
        if self.file_path:
            self.generate_button.config(state=tk.NORMAL)
        else:
            self.generate_button.config(state=tk.DISABLED)

    def update_progress(self, percentage, message=None):
        """Aggiorna la barra di progresso e il messaggio"""
        self.progress_var.set(percentage)
        if message:
            self.progress_label.config(text=message)
        self.master.update_idletasks()  # Forza l'aggiornamento dell'interfaccia

    def cancel_processing(self):
        """Annulla il processo di trascrizione"""
        if self.is_processing:
            self.should_cancel = True
            self.log("Annullamento in corso...")
            self.cancel_button.config(state=tk.DISABLED)
            self.progress_label.config(text="Annullamento in corso...")

    def start_processing(self):
        """Avvia il processo di generazione dei sottotitoli in un thread separato"""
        if not self.file_path:
            messagebox.showwarning("Attenzione", "Seleziona un file prima di procedere.")
            return
        
        # Se non è stata selezionata una destinazione, apri il dialogo
        if not self.output_path:
            self.select_output()
            if not self.output_path:  # Se l'utente ha annullato
                return
                
        # Carica il modello se non è già caricato o se il modello selezionato è diverso
        model_size = self.model_var.get()
        if self.model is None or getattr(self.model, 'model_size', None) != model_size:
            self.load_model(model_size)
            return  # Il caricamento del modello avvierà la trascrizione quando completato
        
        # Avvia il thread di elaborazione
        self.should_cancel = False
        self.is_processing = True
        self.generate_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.update_progress(0, "Inizializzazione...")
        
        threading.Thread(target=self.process_file, daemon=True).start()

    def load_model(self, model_size):
        """Carica il modello Whisper specificato"""
        self.log(f"Caricamento del modello Whisper '{model_size}'...")
        self.generate_button.config(state=tk.DISABLED)
        self.update_progress(0, f"Caricamento modello '{model_size}'...")
        
        def _load():
            try:
                self.model = whisper.load_model(model_size)
                # Salva la dimensione del modello per confronti futuri
                self.model.model_size = model_size
                self.log(f"Modello Whisper '{model_size}' caricato con successo!")
                self.master.after(0, lambda: self.update_progress(0, "Modello caricato! Pronto per la trascrizione."))
                self.master.after(0, lambda: self.start_processing() if self.file_path else None)
            except Exception as e:
                self.log(f"Errore nel caricamento del modello: {e}")
                self.master.after(0, lambda: messagebox.showerror("Errore", f"Errore nel caricamento del modello: {e}"))
                self.master.after(0, lambda: self.update_progress(0, "Errore nel caricamento del modello."))
                self.is_processing = False
        
        self.is_processing = True
        threading.Thread(target=_load, daemon=True).start()

    def process_file(self):
        """Elabora il file selezionato per generare sottotitoli"""
        try:
            self.update_progress(0, "Preparazione file...")
            
            file_path = self.file_path
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            audio_path = file_path
            temp_audio = None

            # Se il file è un video, estrai l'audio in un file temporaneo
            if ext in VIDEO_EXTENSIONS:
                self.log("File video riconosciuto. Estrazione dell'audio...")
                self.update_progress(5, "Estrazione audio dal video...")
                try:
                    temp_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                    audio_path = temp_audio.name
                    temp_audio.close()  # chiude il file per permettere a ffmpeg di scriverci
                    extract_audio_from_video(file_path, audio_path, self.log)
                except Exception as e:
                    self.log(f"Errore durante l'estrazione audio: {e}")
                    self.update_progress(0, "Errore durante l'estrazione audio.")
                    self.is_processing = False
                    self.generate_button.config(state=tk.NORMAL)
                    self.cancel_button.config(state=tk.DISABLED)
                    return

            if self.should_cancel:
                if temp_audio and os.path.exists(audio_path):
                    os.remove(audio_path)
                self.log("Operazione annullata.")
                self.update_progress(0, "Operazione annullata.")
                self.is_processing = False
                self.generate_button.config(state=tk.NORMAL)
                self.cancel_button.config(state=tk.DISABLED)
                return

            self.update_progress(10, "Avvio trascrizione...")
            
            try:
                segments = transcribe_audio_with_progress(
                    audio_path, 
                    self.model, 
                    self.log,
                    lambda progress, msg: self.master.after(0, lambda: self.update_progress(10 + progress * 0.8, msg))
                )
            except Exception as e:
                self.log(f"Errore durante la trascrizione: {e}")
                self.update_progress(0, "Errore durante la trascrizione.")
                self.is_processing = False
                self.generate_button.config(state=tk.NORMAL)
                self.cancel_button.config(state=tk.DISABLED)
                if temp_audio and os.path.exists(audio_path):
                    os.remove(audio_path)
                return

            if self.should_cancel:
                if temp_audio and os.path.exists(audio_path):
                    os.remove(audio_path)
                self.log("Operazione annullata.")
                self.update_progress(0, "Operazione annullata.")
                self.is_processing = False
                self.generate_button.config(state=tk.NORMAL)
                self.cancel_button.config(state=tk.DISABLED)
                return

            # Salvataggio sottotitoli
            self.update_progress(95, "Salvataggio sottotitoli...")
            format_type = self.format_var.get()
            save_subtitles(segments, self.output_path, format_type, self.log)

            # Rimuove il file audio temporaneo, se presente
            if temp_audio and os.path.exists(audio_path):
                os.remove(audio_path)
                self.log("File audio temporaneo rimosso.")

            self.update_progress(100, "Completato!")
            self.log("Operazione completata con successo!")
            messagebox.showinfo("Fatto", f"Sottotitoli generati con successo in:\n{self.output_path}")

        except Exception as e:
            self.log(f"Errore durante l'elaborazione: {e}")
            self.update_progress(0, "Errore durante l'elaborazione.")
            messagebox.showerror("Errore", f"Si è verificato un errore durante l'elaborazione: {e}")
        finally:
            self.is_processing = False
            self.should_cancel = False
            self.generate_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = SubtitleGeneratorGUI(root)
    root.mainloop()