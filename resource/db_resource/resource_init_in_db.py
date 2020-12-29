import asyncpg
import traceback
from asyncpg.exceptions import UniqueViolationError

from ..global_ import Profiler



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

    if is_create:
        print("close postgre pool")
        await postgresql_pool.close()
