import sqlite3

from flask import g

from config import DATABASE_URL


def get_db():
    """Veritabanı bağlantısını açar ve mevcut istek boyunca saklar."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_URL.replace("sqlite:///", ""))
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db(app):
    """Leads tablosunu oluşturur."""
    with app.app_context():
        db = get_db()

        db.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        try:
            db.execute("ALTER TABLE leads ADD COLUMN email TEXT")
        except sqlite3.OperationalError:
            pass

        db.commit()


def lead_ekle(isim, email, telefon, mesaj):
    """Yeni bir lead kaydeder."""

    db = get_db()

    db.execute(
        """
        INSERT INTO leads (isim, email, telefon, mesaj)
        VALUES (?, ?, ?, ?)
        """,
        (isim, email, telefon, mesaj),
    )

    db.commit()


def tum_leadler():
    """Veritabanındaki tüm lead kayıtlarını getirir."""
    db = get_db()

    return db.execute(
        """
        SELECT id, isim, telefon, mesaj, tarih
        FROM leads
        ORDER BY tarih DESC
        """
    ).fetchall()
