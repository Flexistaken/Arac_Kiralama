from services.file_service import load_cars, save_cars


def get_all_cars():
    return load_cars()


def add_car(car_dict):
    cars = load_cars()
    cars.append(car_dict)
    save_cars(cars)


def delete_car(plaka):
    cars = load_cars()
    cars = [car for car in cars if car["plaka"] != plaka]
    save_cars(cars)


def rent_car(plaka, musteri, baslangic, bitis):
    cars = load_cars()

    for car in cars:
        if car["plaka"] == plaka and car["durum"] == "müsait":
            car["durum"] = "kirada"
            car["kiralayan"] = musteri
            car["baslangic_tarihi"] = baslangic
            car["bitis_tarihi"] = bitis
            break

    save_cars(cars)


def return_car_by_plate(plaka):
    cars = load_cars()

    for car in cars:
        if car["plaka"] == plaka and car["durum"] == "kirada":
            car["durum"] = "müsait"
            car["kiralayan"] = ""
            car["baslangic_tarihi"] = ""
            car["bitis_tarihi"] = ""
            save_cars(cars)
            return True

    return False


def update_car(updated_car):
    cars = load_cars()

    for i, car in enumerate(cars):
        if car["plaka"] == updated_car["plaka"]:
            cars[i] = updated_car
            break

    save_cars(cars)