import traceback
from aiohttp import web_request, web
import pymongo
from .models import (
    PostChatData
)

from api_admin.functions.helpers import return_data


async def post_airport_data(request: web_request.Request) -> web.Response:
    code = 200
    resp_data = await return_data()
    headers = {}

    try:
        input_data = PostChatData(data=await request.json())
    except:
        traceback.print_exc()
        resp_data["data"] = dict(request.rel_url.query)
        resp_data["message"] = str(await request.json())
        code = 406
    else:
        myclient = pymongo.MongoClient("mongodb://localhost:27018/")
        mydb = myclient["mydatabase"]
        mycol = mydb["customers"]

        mydict = {"name": input_data.name, "review": input_data.review, "rating": input_data.rating}

        x = mycol.insert_one(mydict)

    print(resp_data, code)
    return web.json_response(resp_data, status=code, headers=headers)

