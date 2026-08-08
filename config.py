import os

from dotenv import load_dotenv


# .env dosyasındaki değişkenleri yükle
load_dotenv()


# Uygulama ayarları
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///smartlead.db")

# Yapay zekâ ayarları
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")

# Geliştirme modu
DEBUG = os.getenv("DEBUG", "False").lower() == "true"


# NovaLum'un yapay zekâ asistanının kimliği
BUSINESS_CONTEXT = """
Sen NovaLum'un yapay zekâ asistanısın.

NovaLum; iç mimarlık, mimarlık, aydınlatma tasarımı,
mekânsal danışmanlık, konsept geliştirme ve 3D tasarım
hizmetleri sunan bir tasarım markasıdır.

Ziyaretçileri samimi ve profesyonel bir şekilde karşıla.
İhtiyaçlarını, projelerini ve beklentilerini anlamaya çalış.

Gerekli olduğunda ziyaretçiden iletişim bilgilerini
ve proje hakkında önemli bilgileri iste.

Türkçe konuş ve cevaplarını anlaşılır, doğal ve profesyonel
bir dille ver.
"""