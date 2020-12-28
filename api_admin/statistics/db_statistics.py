import traceback
from .models import (
    GetAllDataByWeatherAndDate
)


async def db_get_all_data_by_weather_and_data(data: GetAllDataByWeatherAndDate, pool) -> [bool, dict]:
    """
    :param data:
    :param pool:
    :return:
    """

    status = True
    return_data = {}

    query = """
        SELECT type, severity, airport, city, start_time, end_time
        FROM event_description
        JOIN airport_data ON airport_data.airport_code = event_description.airport
        JOIN time_params ON time_params.event_id = event_description.event_id
        WHERE start_time >= {startDate} and end_time <= {endDate} and type = {weather}
        ORDER BY start_time DESC
    """.format(
        startDate=data.start_date,
        endDate=data.end_date,
        weather=data.weather
    )

    try:
        async with pool.acquire() as conn:
            fetch_data = await conn.fetch(query)
    except:
        traceback.print_exc()
        status = False
    else:
        return_data["info"] = [{
            "type": i["type"],
            "severity": i["severity"],
            "airport": i["airport"],
            "city": i["city"],
            "start_date": i["start_date"],
            "end_date": i["end_date"]
        } for i in fetch_data]
    return status, return_data
