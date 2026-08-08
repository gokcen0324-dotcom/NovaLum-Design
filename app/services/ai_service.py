from groq import Groq

from config import BUSINESS_CONTEXT, GROQ_API_KEY


class AIServiceError(Exception):
    """Yapay zekâ servisiyle ilgili hatalar için özel hata sınıfı."""
    pass


class AIService:
    """Groq yapay zekâ servisiyle iletişim kuran sınıf."""

    def __init__(self):
        self.api_key = GROQ_API_KEY

        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None

    def yanit_uret(self, mesaj, gecmis=None):
        """
        Kullanıcı mesajını ve sohbet geçmişini alır,
        Groq'a gönderir ve yapay zekâ cevabını döndürür.
        """

        # API anahtarı yoksa demo modunda çalış
        if not self.api_key:
            return (
                "Şu anda demo modundayım. "
                "Yapay zekâ bağlantısı henüz yapılandırılmadı."
            )

        if gecmis is None:
            gecmis = []

        messages = [
            {
                "role": "system",
                "content": BUSINESS_CONTEXT,
            }
        ]

        # Önceki konuşmaları ekle
        for mesaj_item in gecmis:
            messages.append(mesaj_item)

        # Yeni kullanıcı mesajını ekle
        messages.append(
            {
                "role": "user",
                "content": mesaj,
            }
        )

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )

            return response.choices[0].message.content

        except Exception as exc:
            raise AIServiceError(
                f"Yapay zekâ servisi kullanılırken hata oluştu: {exc}"
            ) from exc


# Uygulamanın kullanacağı AI servis nesnesi
ai_service = AIService()