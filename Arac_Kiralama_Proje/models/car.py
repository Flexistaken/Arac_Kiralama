class Car:
    def __init__(self, plaka, marka, model, ucret, durum="müsait"):
        self.plaka = plaka
        self.marka = marka
        self.model = model
        self.ucret = ucret
        self.durum = durum
        self.kiralayan = ""
        self.baslangic_tarihi = ""
        self.bitis_tarihi = ""

    def to_dict(self):
        return self.__dict__
