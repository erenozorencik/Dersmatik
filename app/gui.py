import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import ttk, messagebox
import os
from .processor import transcribe_audio, generate_summary, generate_questions

class DersmatikApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dersmatik v1.0")
        self.geometry("800x400")
        self.configure(bg="#f0f0f0")
        self.create_widgets()
        self.create_output_folders()

    def create_output_folders(self):
        """Çıktı klasörlerini oluştur"""
        folders = ["transcripts", "summaries", "questions"]
        for folder in folders:
            os.makedirs(f"./outputs/{folder}", exist_ok=True)

    def create_widgets(self):
        """Arayüz bileşenlerini oluştur"""
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        
        # 1. Transkript Bölümü
        trans_frame = ttk.LabelFrame(self, text="🎤 Ses Dosyasını Sürükle → Transkript Oluştur", padding=10)
        trans_frame.pack(pady=10, padx=10, fill="x")
        self.create_drop_zone(trans_frame, self.handle_transcript, "mp3, wav")

        # 2. Özet Bölümü
        sum_frame = ttk.LabelFrame(self, text="📝 Transkripti Sürükle → Özet Oluştur", padding=10)
        sum_frame.pack(pady=10, padx=10, fill="x")
        self.create_drop_zone(sum_frame, self.handle_summary, "txt")

        # 3. Soru Bölümü
        q_frame = ttk.LabelFrame(self, text="❓ Transkripti Sürükle → Soru Oluştur", padding=10)
        q_frame.pack(pady=10, padx=10, fill="x")
        self.create_drop_zone(q_frame, self.handle_questions, "txt")

    def create_drop_zone(self, parent, handler, file_types):
        """Sürükle-bırak alanı oluştur"""
        lbl = tk.Label(parent, text=f"Sürükle → {file_types}", bg="#ffffff", width=50, height=3)
        lbl.pack(pady=5, padx=5)
        parent.drop_target_register(DND_FILES)
        parent.dnd_bind('<<Drop>>', handler)

    def handle_transcript(self, event):
        """Ses dosyası işleme"""
        file_path = self.clean_file_path(event.data)
        if not file_path.lower().endswith((".mp3", ".wav")):
            messagebox.showerror("Hata", "Sadece ses dosyaları kabul edilir!")
            return
        
        try:
            transcript = transcribe_audio(file_path)
            output_path = f"./outputs/transcripts/{os.path.basename(file_path)}.txt"
            print("Kaydedilen dosya yolu:", output_path)  # 🛠 Terminalde görüntüleyin
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(transcript)
            messagebox.showinfo("Başarılı", f"Transkript oluşturuldu:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def handle_summary(self, event):
        """Özet oluşturma"""
        self.process_text_file(event.data, "summary", generate_summary, "./outputs/summaries")

    def handle_questions(self, event):
        """Soru oluşturma"""
        self.process_text_file(event.data, "questions", generate_questions, "./outputs/questions")

    def process_text_file(self, file_path, process_type, processor_func, output_dir):
        """Metin dosyasını işle"""
        file_path = self.clean_file_path(file_path)
        if not file_path.lower().endswith(".txt"):
            messagebox.showerror("Hata", "Sadece TXT dosyaları kabul edilir!")
            return
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            result = processor_func(text)
            output_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_{process_type}.txt"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result)
            
            messagebox.showinfo("Başarılı", f"{process_type.capitalize()} kaydedildi:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    @staticmethod
    def clean_file_path(path: str) -> str:
        """Dosya yolunu temizle"""
        return path.strip().replace("{", "").replace("}", "")

if __name__ == "__main__":
    app = DersmatikApp()
    app.mainloop()