from ..config import BASE_URL

from .airport.api_statistics import (
    get_airport_data,
    get_weather_data
)

from .statistics.api_statistics import (
    get_weather_data_stat
)

from .chat.api_statistics import (
    post_airport_data
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

        self.post_comlain = self.base_url + "/chat"

url = Url(base_url=BASE_URL)

routes = [
    # airport
    ('POST', url.airport_info, get_airport_data, 'info'),
    ('POST', url.airport_weather, get_weather_data, 'weather'),

    # weather
    ('POST', url.get_all_stat, get_weather_data_stat, 'stat'),
    ('POST', url.post_comlain, post_airport_data, 'chat')
]
