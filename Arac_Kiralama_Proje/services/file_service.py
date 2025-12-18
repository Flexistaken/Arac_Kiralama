import json
import os

FILE_PATH = "Arac_Kiralama_Proje/data/cars.json"

def load_cars():
    if not os.path.exists("Arac_Kiralama_Proje/data/cars.json"):
        return []

    with open("Arac_Kiralama_Proje/data/cars.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_cars(cars):
    with open("Arac_Kiralama_Proje/data/cars.json", "w", encoding="utf-8") as f:
        json.dump(cars, f, indent=4, ensure_ascii=False)

def add_car(new_car):
    cars = load_cars()
    cars.append(new_car)
    save_cars(cars)

