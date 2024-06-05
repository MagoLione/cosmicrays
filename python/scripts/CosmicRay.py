import datetime

# A class to save a CosmicRay with a date, an angle, and a description.
class CosmicRay:
    def __init__(self, date: datetime, angle: int, description: str):
        self.date: datetime = date
        self.angle: int = angle
        self.description: str = description