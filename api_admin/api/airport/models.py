from api_admin.models import BaseModel, HasPagination


class GetAirportData(BaseModel):
    def __init__(self, data: dict):
        self.code = str(data["airportCode"])


class GetAirportDataWeather(HasPagination):
    def __init__(self, data: dict):
        super().__init__({"page": data["page"], "limit": data["limit"]})

        self.code = data["airportCode"]
