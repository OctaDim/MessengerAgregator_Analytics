import asyncio
from typing import Optional

from tg_telethon.tlt_manager.telethon_clients_manager import (
    TelethonManager)

telethon_manager: Optional[TelethonManager]


def get_global_telethon_manager_inst():
    """Very important function to get global variable. If not used
    the value may be None depending on import order"""
    global telethon_manager
    return telethon_manager


async def initialise_telethon_manager():
    global telethon_manager
    telethon_manager = TelethonManager()
    telethon_configs = await telethon_manager.get_postgres_db_tlt_configs()
    print(f"####### telethon_manager: {telethon_manager}")
    print(f"####### telethon_configs: {telethon_configs}")
    await telethon_manager.run_all_telethon_clients(telethon_configs)
    await telethon_manager.run_all_tlt_clients_async_tasks()
    return telethon_manager

asyncio.run(main=initialise_telethon_manager(), debug=True)
