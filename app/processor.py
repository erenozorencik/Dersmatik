import os
import openai
from dotenv import load_dotenv
import whisper



# Ortam değişkenlerini yükle
load_dotenv("./config/.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Whisper Modeli (Ücretsiz)
whisper_model = whisper.load_model("base")

def transcribe_audio(file_path: str) -> str:
    """Ses dosyasını metne çevirir (Whisper)"""
    result = whisper_model.transcribe(file_path, language="tr")
    return result["text"]

def generate_summary(text: str) -> str:
    """OpenAI ile özet oluşturur (GPT-3.5 Turbo)"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",  # En ekonomik ve hızlı
        messages=[
            {"role": "system", "content": "Bu metni maksimum 3 cümlede özetle. Dil: Türkçe"},
            {"role": "user", "content": text}
        ],
        max_tokens=50  # Maliyet kontrolü
    )
    return response.choices[0].message.content

def generate_questions(text: str) -> str:
    """OpenAI ile soru oluşturur (GPT-3.5 Turbo)"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "Bu metinden 5 çoktan seçmeli soru üret. Sorular Türkçe olsun."},
            {"role": "user", "content": text}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content