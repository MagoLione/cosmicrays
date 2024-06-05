# A class representing the measurement tool settings.
class Settings:
    def __init__(self, active: bool, angle: int, description: str = None) -> None:
        self.active: bool = active
        self.angle: int = angle
        self.description: str = description
        
# A class to track global public variables.
class Track:
    def __init__(self) -> None:
        self.to_do_list: list = []
        self.is_running: bool = False
        self.count: int = 0
        self.description: str = None
        self.servo_angle: int = 0
        self.active: bool = True
        self.automode: bool = False
        
    def synchronize(self, settings: Settings) -> str:
        self.active = settings.active
        self.servo_angle = settings.angle
        self.description = settings.description
        
        return f"Active: {self.active}\nAngle: {self.servo_angle}\nDescription: {self.description}"
        
    def getSettings(self) -> Settings:
        return Settings(self.active, self.servo_angle, self.description)