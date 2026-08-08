from flask import Flask
from flask_cors import CORS

import config
from app.database import init_db
from app.routes import api, pages


def create_app():
    """Flask uygulamasını oluşturan application factory."""

    app = Flask(__name__)

    # Config ayarlarını yükle
    app.config.from_object(config)

    # CORS'u etkinleştir
    CORS(app)

    # Veritabanını başlat
    init_db(app)

    # Blueprint'leri kaydet
    app.register_blueprint(pages)
    app.register_blueprint(api, url_prefix="/api")

    return app