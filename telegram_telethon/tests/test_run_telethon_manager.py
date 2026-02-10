import asyncio

from telegram_telethon.telethon_clients_manager import TelethonManager


async def main_run_telethon_process():
    telethon_manager = TelethonManager()
    telethon_configs = await telethon_manager.get_postgres_db_tlt_configs()
    print(telethon_configs)
    await telethon_manager.create_authorise_tlt_clients(telethon_configs)
    await telethon_manager.run_all_tlt_clients_tasks()

asyncio.run(main_run_telethon_process(), debug=True)
