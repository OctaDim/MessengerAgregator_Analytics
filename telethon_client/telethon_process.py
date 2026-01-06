import multiprocessing
from telethon import TelegramClient

from configs.settings import (
    TELEGRAM_OFFICIAL_API_ID, TELEGRAM_OFFICIAL_API_HASH,
    TELETHON_OPTIONS)

telegram_client: TelegramClient = None
telethon_process: multiprocessing.Process = None


def create_telethon_client():
    global telegram_client
    telegram_client = TelegramClient(session="TelethonSession",
                                     api_id=TELEGRAM_OFFICIAL_API_ID,
                                     api_hash=TELEGRAM_OFFICIAL_API_HASH)
    telegram_client.disconnect()
    telegram_client.start()
    telegram_client.run_until_disconnected()
    return telegram_client


def start_telethon_process():
    global telethon_process
    telethon_process = multiprocessing.Process(
        target=create_telethon_client)
    telethon_process.start()


def stop_telethon_process():
    if telethon_process and telethon_process.is_alive():
        try:
            telethon_process.terminate()  # Graceful shutdown daughter process
            telethon_process.join(
                timeout=TELETHON_OPTIONS.TERMINATE_PROCESS_TIMEOUT)  # Wait for process to terminate
            print(f"Termination Telethon process [OK]\n")
            if telethon_process.is_alive():
                telethon_process.kill()  # Force kill if still alive
                telethon_process.join(
                    timeout=TELETHON_OPTIONS.KILL_PROCESS_TIMEOUT)
                print(f"Killing Telethon process [WARNING]\n")
        except Exception as error:
            print(f"Stopping telethon process [ERROR]: {error}\n")
        finally:
            if telethon_process:
                telethon_process.close()  # Always close the process object
                print(f"Cleaning Telethon process [OK]\n")
