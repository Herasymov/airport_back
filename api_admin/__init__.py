import aio_pika
import asyncpg
from aiohttp import web
import aioredis


from .config import (
    BASE_URL,
    sync_db,
    global_config
)

from .api import routes, url


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


app = web.Application()
app.on_startup.append(on_start_up_app)
app.on_shutdown.append(on_shutdown_app)
for route in routes:
    app.router.add_route(method=route[0], path=route[1], handler=route[2], name=route[3])
