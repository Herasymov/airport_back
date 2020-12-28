import traceback
from .models import (
    GetAirportData,
    GetAirportWeather
)


async def db_get_airport_data(data: GetAirportData, pool) -> [bool, dict]:
    """
    :param data:
    :param pool:
    :return:
    """

    status = True
    return_data = {}

    query = """
        SELECT *
        FROM airport_data
        WHERE airport_code = {code}
    """.format(
        code=data.code
    )

    try:
        async with pool.acquire() as conn:
            fetch_data = await conn.fetch(query)
    except:
        traceback.print_exc()
        status = False
    else:
        return_data = {
            "code": fetch_data["airport_code"],
            "location_lat": fetch_data["location_lat"],
            "location_lng": fetch_data["location_lng"],
            "city": fetch_data["city"],
            "country": fetch_data["country"],
            "state": fetch_data["state"],
            "zipcode": fetch_data["city"]
        }
    return status, return_data


async def db_get_airport_weather(data: GetAirportWeather, pool) -> [bool, dict]:
    """
    :param data:
    :param pool:
    :return:
    """

    status = True
    return_data = {}

    query = """
        SELECT airport_code, type, severity, start_time, end_time
        FROM airport_data
        JOIN event_description e ON e.airport = airport_data.airport_code
		JOIN time_params ON time_params.event_id = e.event_id
        WHERE airport_code = {code}
		ORDER BY start_time DESC
    """.format(code=data.code)

    try:
        async with pool.acquire() as conn:
            fetch_data = await conn.fetch(query)
    except:
        traceback.print_exc()
        status = False
    else:
        return_data["info"] = [{
            "code": fetch_data["airport_code"],
            "type": i["type"],
            "severity": i["severity"],
            "start_date": i["start_date"],
            "end_date": i["end_date"]
        } for i in fetch_data]

    return status, return_data
