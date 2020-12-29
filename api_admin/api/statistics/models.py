from ...models import HasPagination
from ...config import convert_date_format


class GetAllDataByWeatherAndDate(HasPagination):
    def __init__(self, data: dict):
        super().__init__({"page": data["page"], "limit": data["limit"]})
        self.weather = str(data["weatherType"])
        self.start_date = convert_date_format.convert_string_to_date(date=data["startDate"])
        self.end_date = convert_date_format.convert_string_to_date(date=data["endDate"])

