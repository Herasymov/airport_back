import traceback
from aiohttp import web_request, web

from .models import (
    PostChatData,
    MongoConnection
)

from api_admin.functions.helpers import return_data



async def post_complain(request: web_request.Request) -> web.Response:
    code = 200
    resp_data = await return_data()
    headers = {}

    try:
        mc = MongoConnection()
        input_data = PostChatData(data=await request.json())
    except:
        traceback.print_exc()
        resp_data["data"] = dict(request.rel_url.query)
        resp_data["message"] = str(await request.json())
        code = 406
    else:
        my_dict = {"name": input_data.name, "review": input_data.review, "rating": input_data.rating}
        mc.mycol.insert_one(my_dict)

    print(resp_data, code)
    return web.json_response(resp_data, status=code, headers=headers)


async def get_complains(request: web_request.Request) -> web.Response:
    code = 200
    resp_data = await return_data()
    headers = {}

    try:
        mc = MongoConnection()
    except:
        traceback.print_exc()
        resp_data["data"] = dict(request.rel_url.query)
        resp_data["message"] = str(await request.json())
        code = 406
    else:
        resp_data["data"] = [{
            'name': doc['name'],
            'review': doc['review'],
            'rating':doc['rating']
        } for doc in mc.mycol.find()]

    return web.json_response(resp_data, status=code, headers=headers)

