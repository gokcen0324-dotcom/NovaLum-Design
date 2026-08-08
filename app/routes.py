import config
import json
from urllib.request import Request, urlopen

from flask import Blueprint, jsonify, render_template, request

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import AIServiceError, ai_service


# Sayfa Blueprint'i
pages = Blueprint("pages", __name__)

# API Blueprint'i
# /api prefix'i __init__.py içinde verilecek.
api = Blueprint("api", __name__)


# =========================================================
# SAYFALAR
# =========================================================

@pages.get("/")
def index():
    """Ana sayfayı gösterir."""
    return render_template("index.html")


@pages.get("/dashboard")
def dashboard():
    """Yönetim panelini gösterir."""
    leads = tum_leadler()

    return render_template(
        "dashboard.html",
        leads=leads,
    )


@pages.get("/health")
def health():
    """Backend'in çalışıp çalışmadığını kontrol eder."""
    return jsonify(
        {
            "status": "ok"
        }
    ), 200


# =========================================================
# AI API
# =========================================================

@api.post("/sohbet")
def sohbet():
    """Kullanıcı mesajını yapay zekâya gönderir."""

    data = request.get_json(silent=True) or {}

    mesaj = data.get("mesaj", "").strip()
    gecmis = data.get("gecmis", [])

    if not mesaj:
        return jsonify(
            {
                "error": "Mesaj alanı zorunludur."
            }
        ), 400

    if not isinstance(gecmis, list):
        gecmis = []

    try:
        yanit = ai_service.yanit_uret(
            mesaj,
            gecmis,
        )

        return jsonify(
            {
                "yanit": yanit
            }
        ), 200

    except AIServiceError:
        return jsonify(
            {
                "error": "Yapay zekâ servisine şu anda ulaşılamıyor."
            }
        ), 503

    except Exception:
        return jsonify(
            {
                "error": "Beklenmeyen bir hata oluştu."
            }
        ), 500


# =========================================================
# LEAD API
# =========================================================

@api.post("/leads")
def create_lead():
    """Yeni bir lead kaydeder ve Google Sheets'e gönderir."""

    data = request.get_json(silent=True) or {}

    isim = data.get("isim", "").strip()
    email = data.get("email", "").strip()
    telefon = data.get("telefon", "").strip()
    mesaj = data.get("mesaj", "").strip()

    if not isim or not telefon:
        return jsonify(
            {
                "error": "İsim ve telefon alanları zorunludur."
            }
        ), 400

    try:
        # 1. Önce kendi veritabanımıza kaydet
        lead_ekle(
            isim,
            telefon,
            mesaj,
        )

        # 2. Google Sheets'e gönder
        sheets_url = config.GOOGLE_SHEETS_WEBHOOK_URL

        if sheets_url:
            sheets_data = json.dumps(
                {
                    "first_name": isim,
                    "email": email,
                    "edde": telefon,
                    "long_answer": mesaj,
                }
            ).encode("utf-8")

            sheets_request = Request(
                sheets_url,
                data=sheets_data,
                headers={
                    "Content-Type": "application/json"
                },
                method="POST",
            )

            sheets_response = urlopen(
                sheets_request,
                timeout=10,
            )

            print(
                "Google Sheets cevabı:",
                sheets_response.read().decode("utf-8")
            )

        return jsonify(
            {
                "message": "Lead başarıyla kaydedildi."
            }
        ), 201

    except Exception as error:
        print("Lead kaydetme hatası:", error)

        return jsonify(
            {
                "error": "Lead kaydedilirken bir hata oluştu."
            }
        ), 500


@api.get("/leads")
def get_leads():
    """Tüm lead kayıtlarını getirir."""

    try:
        leads = tum_leadler()

        return jsonify(
            [
                dict(lead)
                for lead in leads
            ]
        ), 200

    except Exception:
        return jsonify(
            {
                "error": "Lead kayıtları alınırken bir hata oluştu."
            }
        ), 500