import asyncio

from tg_telethon.tlt_manager.telethon_clients_manager import TelethonManager

async def main_run_telethon_process():
    global telethon_manager
    telethon_manager = TelethonManager()
    telethon_configs = await telethon_manager.get_postgres_db_tlt_configs()
    print(f"####### telethon_manager: {telethon_manager}")
    print(f"####### telethon_configs: {telethon_configs}")
    await telethon_manager.run_all_telethon_clients(telethon_configs)
    await telethon_manager.run_all_tlt_clients_async_tasks()
    # await tlt_manager.disconnect_all_tlt_clients()
    print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@ telethon_manager: {telethon_manager}")
    return telethon_manager


asyncio.run(main_run_telethon_process(), debug=True)
