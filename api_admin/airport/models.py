from ..models import BaseModel


class GetAirportData(BaseModel):
    def __init__(self, data: dict):
        self.code = str(data["airportCode"])


class GetAirportWeather(BaseModel):
    def __init__(self, data: dict):
        self.code = str(data["airportCode"])
