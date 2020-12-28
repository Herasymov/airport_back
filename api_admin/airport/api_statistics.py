import traceback
from aiohttp import web_request, web

from .models import (
    GetAirportData,
    GetAirportWeather
)

from .db_statistics import (
    db_get_airport_data,
    db_get_airport_weather
)

from ..functions.helpers import return_data


async def get_airport_data(request: web_request.Request) -> web.Response:
    code = 200
    resp_data = await return_data()
    headers = {}

    try:
        input_data = GetAirportData(data=await request.json())
    except:
        traceback.print_exc()
        resp_data["data"] = dict(request.rel_url.query)
        resp_data["message"] = str(await request.json())
        code = 406
    else:
        status, data = await db_get_airport_data(data=input_data, pool=request.app["pool"])
        if status:
            resp_data["data"] = data
        else:
            code = 500

    print(resp_data, code)
    return web.json_response(resp_data, status=code, headers=headers)


async def get_weather_data(request: web_request.Request) -> web.Response:
    code = 200
    resp_data = await return_data()
    headers = {}

    try:
        input_data = GetAirportWeather(data=await request.json())
    except:
        traceback.print_exc()
        resp_data["data"] = dict(request.rel_url.query)
        resp_data["message"] = str(await request.json())
        code = 406
    else:
        status, data = await db_get_airport_weather(data=input_data, pool=request.app["pool"])
        if status:
            resp_data["data"] = data
        else:
            code = 500

    print(resp_data, code)
    return web.json_response(resp_data, status=code, headers=headers)