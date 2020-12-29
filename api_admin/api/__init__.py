from ..config import BASE_URL

from .airport.api_statistics import (
    get_airport_data,
    get_weather_data
)

from .statistics.api_statistics import (
    get_weather_data_stat
)


class Url:
    def __init__(self, base_url: str):
        self.base_url = base_url
        if self.base_url[0] != "/" or self.base_url[-1] == "/":
            raise ValueError(f"not valid base url {base_url}")

        # airport
        self.airport_weather = self.base_url + "/airport/weather"
        self.airport_info = self.base_url + "/airport/info"

        # statistics
        self.get_all_stat = self.base_url + "/statistics/stat"


url = Url(base_url=BASE_URL)

routes = [
    # airport
    ('GET', url.airport_info, get_airport_data, 'info'),
    ('GET', url.airport_weather, get_weather_data, 'weather'),

    # weather
    ('GET', url.get_all_stat, get_weather_data_stat, 'stat')
]
