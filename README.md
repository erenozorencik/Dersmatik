# Dersmatik
Ses dosyalarını metne çevirebilen transkript edilen içeriği yapay zeka yardımı ile özet haline dönüştürebilen ve konu hakkında örnek sorular üretebilen araç.

Bir ses dosyasını "Transkript Oluştur" bölümüne sürükleyin → outputs/transcripts/ altında TXT dosyası oluşur.

Oluşan TXT dosyasını "Özet Oluştur" bölümüne sürükleyin → outputs/summaries/ altında özet kaydedilir.

Aynı TXT dosyasını "Soru Oluştur" bölümüne sürükleyin → outputs/questions/ altında sorular kaydedilir.

## Kurulum
1. `pip install -r requirements.txt`
2. `config/.env` dosyasına OpenAI API anahtarınızı ekleyin.

## Kullanım
`python -m app.gui`