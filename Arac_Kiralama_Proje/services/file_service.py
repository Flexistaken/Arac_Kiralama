import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "cars.json")

def load_cars():
    if not os.path.exists("data/cars.json"):
        return []

    with open("data/cars.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_cars(cars):
    with open("data/cars.json", "w", encoding="utf-8") as f:
        json.dump(cars, f, indent=4, ensure_ascii=False)

def add_car(new_car):
    cars = load_cars()
    cars.append(new_car)
    save_cars(cars)

