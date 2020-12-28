import aio_pika
import asyncpg
from aiohttp import web
import colored
from colored import stylize
import aioredis


from .functions.helpers import token_to_data
from .config import (
    composer,
    lang as l,
    BASE_URL,
    sync_db,
    global_config
)

from .api import routes, url


@web.middleware
async def locale_middleware(request, handler):
    lang = request.headers.get("Accept-Language", l.default_language)
    if lang not in l.available_languages:
        lang = l.default_language
    request["language"] = lang
    print(request["language"])
    return await handler(request=request)


@web.middleware
async def session_middleware(request, handler):
    # красиво в консоли отображает текущий урл запроса
    print(stylize(str(request.path), colored.fg("green")))
    print(request.headers.get("token"))
    if url.protected_entry.get(request.path):
        if not request.headers.get("token", False):
            return web.json_response(data={"message": composer(request["language"]).error_401_response},
                                     status=401)

        is_good, data = await token_to_data(token=request.headers["token"],
                                            redis_pool=request.app["redis_session_key"])
        print("TOKEN DATA ::", data)
        if not is_good:
            return web.json_response(data={"message": composer(request["language"]).error_401_response},
                                     status=401)

        if url.root_only.get(request.path) and not data["isRoot"]:
            return web.json_response(data={"message": composer(request["language"]).error_401_response},
                                     status=401)
        request["tokenData"] = data
    return await handler(request=request)


async def on_start_up_app(app):

    app['redis_session_key'] = await aioredis.create_redis_pool(
        address=(global_config.redisSessionKey.host,
                 global_config.redisSessionKey.port),
        db=global_config.redisSessionKey.db,
        encoding=global_config.redisSessionKey.encoding)

    # TODO different db users
    app['pool'] = await asyncpg.create_pool(
        database=global_config .postgreSettings.dbname,
        user=global_config .postgreSettings.user,
        password=global_config .postgreSettings.password,
        host=global_config.postgreSettings.host,
        port=global_config .postgreSettings.port,
        min_size=5,
        max_size=5
    )

    await sync_db(postgresql_pool=app['pool'])

    app['rabbit_connect'] = await aio_pika.connect_robust(
        url=global_config .rabbitMqSetting.url,
        port=global_config.rabbitMqSetting.port)

    channel = await app['rabbit_connect'].channel(publisher_confirms=False)
    exchange = await channel.declare_exchange('autoparts', auto_delete=False)
    app["exchange"] = exchange


async def on_shutdown_app(app_):
    app_['redis_session_key'].close()
    await app_['redis_session_key'].wait_closed()

    await app_['pool'].close()

    await app_['rabbit_connect'].close()


app = web.Application(middlewares=[locale_middleware, session_middleware])
app.on_startup.append(on_start_up_app)
app.on_shutdown.append(on_shutdown_app)
for route in routes:
    app.router.add_route(method=route[0], path=route[1], handler=route[2], name=route[3])
