import asyncio
import os.path
from typing import Optional

from configs.settings import TELETHON_OPTIONS, BASE_DIR
from tg_telethon.tlt_manager.telethon_clients_manager import (
    TelethonManager)
from utils_common.normalized_path import (
    get_full_dir_normal_path)

telethon_manager: Optional[TelethonManager]


def get_global_telethon_manager_inst():
    """Very important function to get global variable. If not used
    the value may be None depending on import order"""
    global telethon_manager
    return telethon_manager


async def init_telethon_sessions_dir():
    telethon_sessions_dir = TELETHON_OPTIONS.BASE_TELETHON_SESSIONS_DIR
    tlt_sessions_dir_full_f_path = get_full_dir_normal_path(
        all_dir_str_parts=[BASE_DIR, telethon_sessions_dir])
    if not os.path.isdir(tlt_sessions_dir_full_f_path):
        os.makedirs(name=tlt_sessions_dir_full_f_path, exist_ok=True)


async def initialise_telethon_manager():
    global telethon_manager

    await init_telethon_sessions_dir()
    telethon_manager = TelethonManager()
    telethon_configs = await telethon_manager.get_postgres_db_tlt_configs()
    print(f"####### telethon_manager: {telethon_manager}")
    print(f"####### telethon_configs: {telethon_configs}")
    await telethon_manager.run_all_telethon_clients(telethon_configs)
    await telethon_manager.run_all_tlt_clients_async_tasks()
    return telethon_manager


asyncio.run(main=initialise_telethon_manager(), debug=True)
