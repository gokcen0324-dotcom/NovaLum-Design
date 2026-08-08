# NovaLum AI

NovaLum AI, yapay zekâ teknolojisini iç mimarlık ve aydınlatma tasarımıyla birleştiren web tabanlı bir tasarım platformudur.

Kullanıcılar tasarlamak istedikleri mekânı doğal dil kullanarak anlatır. Sistem, kullanıcı ile yapay zekâ arasında etkileşimli bir sohbet oluşturarak mekânın ihtiyaçlarını adım adım belirler ve tasarım sürecine yönelik öneriler sunar.

## Proje Özeti

NovaLum AI temel olarak:

- Kullanıcıdan mekân ve tasarım ihtiyaçlarını alır.
- Kullanıcı ile yapay zekâ arasında sohbet oluşturur.
- Önceki mesajları konuşma geçmişinde tutar.
- Kullanıcının verdiği bilgilere göre yeni sorular sorar.
- Yapay zekâ destekli tasarım önerileri üretir.
- Sonuçları web sitesi üzerindeki sohbet arayüzünde gösterir.

## Kullanılan Teknolojiler

### Frontend
- Wix Studio
- Velo
- JavaScript

### Backend
- Python
- Flask
- REST API

### Yapay Zekâ
- Groq API

### Veritabanı
- SQLite

### Yayınlama
- GitHub
- Render

## Sistem Mimarisi

Proje frontend ve backend olmak üzere iki temel bölümden oluşmaktadır.

### Frontend

Kullanıcı arayüzü Wix Studio üzerinde oluşturulmuştur. Wix Velo kullanılarak kullanıcı mesajları backend API'sine gönderilir ve backend'den gelen yapay zekâ cevapları sohbet arayüzünde gösterilir.

### Backend

Backend Python ve Flask kullanılarak geliştirilmiştir. Flask API, Wix Studio'dan gelen kullanıcı mesajlarını alır, yapay zekâ servisi ile iletişim kurar ve oluşturulan cevabı frontend'e gönderir.

### Genel Akış

Kullanıcı

↓

Wix Studio / Velo

↓

Flask API

↓

Groq AI

↓

Flask API

↓

Wix Studio

↓

Kullanıcı

## Proje Yapısı

```text
NovaLum Design/
│
├── app/
│   ├── services/
│   │   └── ai_service.py
│   ├── templates/
│   ├── __init__.py
│   ├── database.py
│   └── routes.py
│
├── config.py
├── requirements.txt
├── run.py
├── .gitignore
└── README.md