class User:
    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id
        self.cars = []
        self.crew = []

class Car:
    def __init__(self, model, car_id):
        self.model = model
        self.car_id = car_id
        self.parts = []
