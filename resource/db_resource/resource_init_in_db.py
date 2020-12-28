import asyncpg
import traceback
from asyncpg.exceptions import UniqueViolationError

from .default_values import DefaultLanguage, DefaultStarSign
from .default_status import DefaultUserProfileStatus, DefaultSendFeelingStatus, DefaultSendFeelingAction
from .default_types import DefaultFeeling

from ..global_ import Profiler


__SYNC_THIS__ = [
    DefaultLanguage(),
    DefaultStarSign(),
    DefaultUserProfileStatus(),
    DefaultFeeling(),
    DefaultSendFeelingStatus(),
    DefaultSendFeelingAction()
]

async def sync_db(postgresql_pool=None):
    print("sync DB")

    is_create = False
    if not postgresql_pool:
        # TODO import
        print("create postgre pool")
        is_create = True
        postgresql_pool = await asyncpg.create_pool(
            database=global_config .postgreSettings.dbname,
            user=global_config .postgreSettings.user,
            password=global_config .postgreSettings.password,
            host=global_config.postgreSettings.host,
            port=global_config .postgreSettings.port,
            min_size=1,
            max_size=1
        )

    p = Profiler()

    async with postgresql_pool.acquire() as conn:
            with p:
                for model in __SYNC_THIS__:
                    print("\tsync model::", model.__class__.__name__)
                    for query in model.insert_on_conflict_update():
                        try:
                            await conn.execute(query[0])
                        except UniqueViolationError:
                            await conn.execute(query[1])
                        except:
                            traceback.print_exc()
                            raise ValueError

    if is_create:
        print("close postgre pool")
        await postgresql_pool.close()
