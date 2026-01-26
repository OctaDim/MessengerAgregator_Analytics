from typing import Dict, Optional, List, Literal

import qrcode
from pydantic import BaseModel
from telethon import TelegramClient
from telethon.sessions import StringSession, SQLiteSession

from configs.enums import (
    TELEGRAM_ACCOUNT_TYPE, QR_CODE_ERROR_CORRECTION)
from configs.settings import ALCHEMY_OPTIONS, TELETHON_OPTIONS
from db_postgres.postgres_conn.pgs_connection import PgsAsyncConnection
from db_postgres.postgres_conn.postgres_session import PgsAsyncSession
from db_postgres.postgres_queries.qry_get_telethon_configs_objs import (
    get_telethon_configs_objs_qry)


class TelethonConfig(BaseModel):
    web_account_id: str
    web_account_username: str
    telethon_config_id: int
    name: str = None
    account_type: TELEGRAM_ACCOUNT_TYPE
    api_id: Optional[int] = None
    api_hash: Optional[str] = None
    session_string: Optional[str] = None
    bot_token: Optional[str] = None
    phone: Optional[str] = None
    proxy: Optional[dict] = None
    is_active: bool = True


class TelethonManager:
    def __init__(self):
        self.clients: Dict[str, TelegramClient] = {}
        # self.clients_configs: List[Dict[str, any]] = []
        self.event_handlers: list[str] = []
        self.running = False

    async def get_db_telethon_configs(self) -> List[TelethonConfig]:
        log_pgs_good_ops = ALCHEMY_OPTIONS.ALCHEMY_SESSION_OK_ACTIONS_LOGS
        pgs_conn = PgsAsyncConnection()
        async with PgsAsyncSession(engine=pgs_conn.engine,
                                   log_good_ops=log_pgs_good_ops
                                   ) as pgs_session:
            pgs_telethon_configs_objs = await get_telethon_configs_objs_qry(
                ongoing_session=pgs_session)

        pgs_telethon_configs_list = []
        for cur_config_obj in pgs_telethon_configs_objs:
            telethon_account_type = cur_config_obj.tg_account_type

            new_config_name = await self.create_new_session_name(
                telethon_db_config_id=cur_config_obj.id,
                web_account_id=cur_config_obj.web_account_id,
                web_account_username=cur_config_obj.web_account_username,
                telethon_account_type=telethon_account_type)

            cur_telethon_config = TelethonConfig(
                telethon_config_id=cur_config_obj.id,
                web_account_id=cur_config_obj.web_account_id,
                web_account_username=cur_config_obj.web_account_username,
                name=new_config_name,
                account_type=cur_config_obj.tg_account_type,
                api_id=cur_config_obj.tg_api_id,
                api_hash=cur_config_obj.tg_api_hash,
                session_string=cur_config_obj.telethon_session_str,
                bot_token=cur_config_obj.tg_bot_token,
                phone=cur_config_obj.tg_personal_phone,
                proxy=cur_config_obj.telethon_proxy_config,
                is_active=cur_config_obj.telethon_is_active)
            pgs_telethon_configs_list.append(cur_telethon_config)
        return pgs_telethon_configs_list

    async def create_new_session_name(
            self,
            telethon_db_config_id: int,
            web_account_id: str,
            web_account_username: str,
            telethon_account_type: Literal[
                TELEGRAM_ACCOUNT_TYPE.ACCOUNT,
                TELEGRAM_ACCOUNT_TYPE.BOT],
    ) -> str:
        if telethon_account_type:
            new_session_name = (f"id_{telethon_db_config_id}_"
                                f"type_{telethon_account_type}_"
                                f"acc_{web_account_id}_{web_account_username}")
        else:
            new_session_name = (f"undefined_{telethon_db_config_id}_"
                                f"{web_account_id}_{web_account_username}")
        return new_session_name

    async def run_all_telethon_clients(
            self, telethon_configs: List[TelethonConfig]
    ) -> None:
        print(f"Running all telethon telegram clients by list:")
        previous_is_bot_flag = False
        for cur_config in telethon_configs:
            account_type = cur_config.account_type
            config_name = cur_config.name
            phone = cur_config.phone

            try:
                if account_type == TELEGRAM_ACCOUNT_TYPE.ACCOUNT:
                    print(f"\n>>>>>>> START PERSONAL ACCOUNT TELETHON CLIENT:\n"
                          f"account_type: {account_type}\n")
                    cur_client = await self.create_telethon_user_client(
                        telethon_config=cur_config)
                    previous_is_bot_flag = False
                elif account_type == TELEGRAM_ACCOUNT_TYPE.BOT:
                    print(f"\n>>>>>>> START TELEGRAM BOT TELETHON CLIENT:\n"
                          f"account_type: {account_type}\n")

                    if previous_is_bot_flag:
                        delay_seconds = TELETHON_OPTIONS.EACH_CLIENT_STARTUP_DELAY_SEC
                        print(f"Waiting before starting next bot client...\n"
                              f"delay_seconds: {delay_seconds}\n"
                              f"previous_is_bot_flag: {previous_is_bot_flag}\n")
                        await asyncio.sleep(delay_seconds)

                    cur_client = await self.create_telethon_bot_client(
                        telethon_config=cur_config)
                    previous_is_bot_flag = True
                else:  # Telethon account type not defined
                    print(f"Telethon client with empty account_type skipped [ERROR]\n"
                          f"account_type: {account_type}\n"
                          f"config_name: {config_name}\n"
                          f"phone: {phone}\n")
                    continue

                if cur_client:
                    self.clients[config_name] = cur_client
                else:
                    print(f"Not authorised and skipped Telethon client [ERROR]\n"
                          f"cur_client: {cur_client}\n")

                    continue
            except Exception as error:
                error_log = (f"Run multiple Telethon clients [ERROR]: \n"
                             f"error: {error}\n")
                print(error_log)

        print(f"\nTelethon clients started successfully [OK]:")
        for cur_config, cur_client in self.clients.items():
            print(f"cur_config: {cur_config}, cur_client: {cur_client}")

    async def create_telethon_user_client(
            self,
            telethon_config: TelethonConfig
    ) -> TelegramClient | None:
        print("Creating existing or new Telethon session:")
        session_string = telethon_config.session_string

        if session_string:
            session = StringSession(string=session_string)
            print(f"Existing Telethon session used via StringSession [OK]:\n"
                  f"session_string: {session_string}\n"
                  f"session: {session}\n")
        else:
            session_prefix = TELETHON_OPTIONS.NEW_SESSION_FILE_PREFIX
            config_name = telethon_config.name
            new_session_id = f"{session_prefix}{config_name}"
            session = SQLiteSession(session_id=new_session_id)
            print(f"New Telethon session created via SQLiteSession [OK]:\n"
                  f"session_string: {session_string}\n"
                  f"config_name: {config_name}\n"
                  f"new_session_id: {new_session_id}\n"
                  f"session: {session}\n")

        user_client = TelegramClient(
            session=session,
            api_id=telethon_config.api_id,
            api_hash=telethon_config.api_hash,
            proxy=telethon_config.proxy,
            connection_retries=5,
            request_retries=5,
            flood_sleep_threshold=120, )

        before_connect_is_connected = user_client.is_connected()
        print(f"Telethon user client state before connect():\n"
              f"before_connect_is_connected: {before_connect_is_connected}\n")

        if not before_connect_is_connected:
            await user_client.connect()

        after_connect_is_connected = user_client.is_connected()
        after_connect_is_authorised = await user_client.is_user_authorized()
        print(f"Telethon user client state after connect():\n"
              f"after_connect_is_connected: {after_connect_is_connected}\n"
              f"after_connect_is_authorised: {after_connect_is_authorised}\n")

        if not after_connect_is_authorised:
            await self.authorise_client_user(
                telethon_user_client=user_client,
                telethon_config=telethon_config)
            after_auth_is_connected = user_client.is_connected()
            after_auth_is_authorised = await user_client.is_user_authorized()
            print(f"Telethon user client state after authorise_client_user():\n"
                  f"after_auth_is_connected: {after_auth_is_connected}\n"
                  f"after_auth_is_authorised: {after_auth_is_authorised}\n")
            if after_auth_is_authorised:
                return user_client
        else:
            print(f"Telethon user client initially authorised:\n"
                  f"after_connect_is_connected: {after_connect_is_connected}\n"
                  f"after_connect_is_authorised: {after_connect_is_authorised}\n")
            return user_client

    async def authorise_client_user(
            self,
            telethon_user_client: TelegramClient,
            telethon_config: TelethonConfig
    ) -> bool:
        config_name = telethon_config.name
        telegram_phone = telethon_config.phone
        user_client = telethon_user_client
        client_is_user_authorised = await user_client.is_user_authorized()
        if client_is_user_authorised:
            return True

        auth_type_choice = None
        request_sent_code = None
        phone_signed_in_user = None
        qr_code_login = None
        qr_code = None
        session_string = None
        qrcode_signed_in_user = None
        try:
            auth_type_choice = input(f"Выберите метод авторизации для "
                                     f"[{telegram_phone}]-[{config_name}]:\n"
                                     f"1 - по телефону \n"
                                     f"2 - QR code \n"
                                     f"3 - пропустить клиента\n"
                                     f"Введите ваш выбор: ")

            if auth_type_choice == "1" and telegram_phone:
                print("Telethon user client authorising via phone")
                request_sent_code = await user_client.send_code_request(
                    phone=telegram_phone,
                    force_sms=False,  # Depricated
                    _retry_count=0)
                print(f"Phone authorisation code sent to phone [OK]:\n"
                      f"request_sent_code: {request_sent_code}\n")

                phone_auth_code = input("Введите код из Telegram: ")
                phone_signed_in_user = await user_client.sign_in(
                    phone=telegram_phone,
                    code=phone_auth_code,
                    password=None,
                    bot_token=None,
                    phone_code_hash=None)
                print(f"Phone user client authorised successfully [OK]:\n"
                      f"request_sent_code: {request_sent_code}\n"
                      f"phone_signed_in_user: {phone_signed_in_user}\n")
                authorised_user_flag = True
            elif auth_type_choice == "2":
                print("Telethon user client authorisation via QR code")
                qr_code_login = await user_client.qr_login(
                    ignored_ids=None)
                print(f"####### QR Сode object: {qr_code_login}")
                print(f"####### QR Code url: {qr_code_login.url}")

                print("Generating QR code in console")
                qr_code = qrcode.QRCode(
                    version=None,
                    error_correction=QR_CODE_ERROR_CORRECTION.LEVEL_M.value,
                    box_size=10,
                    border=4,
                    image_factory=None,
                    mask_pattern=None, )
                qr_code.add_data(qr_code_login.url, optimize=20)
                qr_code.print_ascii()
                qrcode_signed_in_user = await qr_code_login.wait()
                print(f"QR Code user client authorised successfully [OK]:\n"
                      f"qr_code_login: {qr_code_login}\n"
                      f"qr_code: {qr_code}\n"
                      f"qrcode_signed_in_user: {qrcode_signed_in_user}\n")
                authorised_user_flag = True
            else:
                authorised_user_flag = False

            if authorised_user_flag:
                print("Telethon obtaining user client session string:")
                session_string = user_client.session.save()
                print("####### session_string: ", session_string)
                # await self.save_session_to_db(config.name, session_string)
                return True
            return False
        except Exception as error:
            error_log = (f"Telethon User Client authorisation [ERROR]: \n"
                         f"error: {error}\n"
                         f"auth_type_choice: {auth_type_choice}\n"
                         f"request_sent_code: {request_sent_code}\n"
                         f"phone_signed_in_user: {phone_signed_in_user}\n"
                         f"qr_code_login: {qr_code_login}\n"
                         f"qr_code: {qr_code}\n"
                         f"qrcode_signed_in_user: {qrcode_signed_in_user}\n"
                         f"session_string: {session_string}\n"
                         f"auth_type_choice: {auth_type_choice}\n")
            print(error_log)
            return False

    @staticmethod
    async def create_telethon_bot_client(
            telethon_config: TelethonConfig
    ) -> TelegramClient | None:
        session_prefix = TELETHON_OPTIONS.NEW_SESSION_FILE_PREFIX
        config_name = telethon_config.name
        new_session_id = f"{session_prefix}{config_name}"
        bot_client = TelegramClient(
            session=new_session_id,
            api_id=telethon_config.api_id,
            api_hash=telethon_config.api_hash,
            proxy=telethon_config.proxy, )

        before_start_is_connected = bot_client.is_connected()
        print(f"Telethon bot client state before start():\n"
              f"before_start_is_connected: {before_start_is_connected}\n")

        if not before_start_is_connected:
            await bot_client.start(  # Bug: await is necessary. Error without await but sync start()
                bot_token=telethon_config.bot_token,
                force_sms=False,
                code_callback=None,
                first_name="New User",
                last_name="",
                max_attempts=3)

        after_start_is_connected = bot_client.is_connected()
        after_start_is_authorised = await bot_client.is_user_authorized()
        after_start_is_bot = await bot_client.is_bot()
        print(f"Telethon user client state after start():\n"
              f"after_start_is_connected: {after_start_is_connected}\n"
              f"after_start_is_authorised: {after_start_is_authorised}\n"
              f"after_start_is_bot: {after_start_is_bot}\n")
        if after_start_is_authorised:
            return bot_client
        return None


import asyncio


async def main_telethon_process():
    telethon_manager = TelethonManager()
    telethon_configs = await telethon_manager.get_db_telethon_configs()
    print(telethon_configs)
    await telethon_manager.run_all_telethon_clients(telethon_configs)


asyncio.run(main_telethon_process(), debug=True)
