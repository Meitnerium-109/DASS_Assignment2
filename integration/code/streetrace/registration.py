from streetrace.models import User, Car

class RegistrationModule:
    """Handles the registration of users and cars."""
    def __init__(self):
        self.users = {}
        self.cars = {}

    def register_user(self, username, user_id):
        if user_id in self.users:
            raise ValueError("User ID already exists.")
        user = User(username, user_id)
        self.users[user_id] = user
        return user

    def register_car(self, user_id, model, car_id):
        if car_id in self.cars:
            raise ValueError("Car ID already exists.")
        if user_id not in self.users:
            raise ValueError("User not found.")
        
        car = Car(model, car_id)
        self.cars[car_id] = car
        self.users[user_id].cars.append(car)
        return car
