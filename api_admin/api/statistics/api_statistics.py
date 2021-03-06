import traceback
from aiohttp import web_request, web

from .models import (
    GetAllDataByWeatherAndDate
)

from.db_statistics import (
    db_get_all_data_by_weather_and_data
)
from api_admin.functions.helpers import return_data

async def get_weather_data_stat(request: web_request.Request) -> web.Response:
    code = 200
    resp_data = await return_data()
    headers = {}

    try:
        input_data = GetAllDataByWeatherAndDate(data=await request.json())
    except:
        traceback.print_exc()
        resp_data["data"] = dict(request.rel_url.query)
        resp_data["message"] = str(await request.json())
        code = 406
    else:
        status, data = await db_get_all_data_by_weather_and_data(data=input_data, pool=request.app["pool"])
        if status:
            resp_data["data"] = data
        else:
            code = 500

    print(resp_data, code)
    return web.json_response(resp_data, status=code, headers=headers)