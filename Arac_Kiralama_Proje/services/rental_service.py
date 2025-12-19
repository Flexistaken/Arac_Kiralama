import json
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENTALS_PATH = os.path.join(BASE_DIR, "data", "rentals.json")


def load_rentals():
    if not os.path.exists(RENTALS_PATH):
        return []
    with open(RENTALS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rentals(rentals):
    with open(RENTALS_PATH, "w", encoding="utf-8") as f:
        json.dump(rentals, f, ensure_ascii=False, indent=4)


def add_rental_record(plaka, musteri, baslangic, bitis, gunluk_ucret):
    """
    baslangic / bitis: 'YYYY-MM-DD' string
    gunluk_ucret: int
    """
    start_dt = datetime.strptime(baslangic, "%Y-%m-%d").date()
    end_dt = datetime.strptime(bitis, "%Y-%m-%d").date()
    gun_sayisi = (end_dt - start_dt).days + 1
    toplam_ucret = gun_sayisi * int(gunluk_ucret)

    record = {
        "plaka": plaka,
        "musteri": musteri,
        "baslangic": baslangic,
        "bitis": bitis,
        "gun_sayisi": gun_sayisi,
        "gunluk_ucret": int(gunluk_ucret),
        "toplam_ucret": toplam_ucret,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    rentals = load_rentals()
    rentals.append(record)
    save_rentals(rentals)
