from ..config import BASE_URL

from .airport.api_statistics import (
    get_airport_data,
    get_weather_data
)

from .statistics.api_statistics import (
    get_weather_data_stat
)

from .chat.api_statistics import (
    post_complain,
    get_complains
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

        #chat
        self.post_comlain = self.base_url + "/chat"
        self.get_complains = self.base_url + "/chat/getComplains"


url = Url(base_url=BASE_URL)

routes = [
    # airport
    ('POST', url.airport_info, get_airport_data, 'info'),
    ('POST', url.airport_weather, get_weather_data, 'weather'),

    # weather
    ('POST', url.get_all_stat, get_weather_data_stat, 'stat'),

    #chat
    ('POST', url.post_comlain, post_complain, 'chat'),
    ('GET', url.get_complains, get_complains, 'getComplains')

]
