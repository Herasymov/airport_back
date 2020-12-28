from ..models import BaseModel


class GetAllDataByWeatherAndDate(BaseModel):
    def __init__(self, data:dict):
        self.weather = str(data["weatherType"])
        self.start_date = data["startDate"]
        self.end_date = data["endDate"]
