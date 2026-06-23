import os
import sys
from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from utils_common.get_cur_ip_address import (
    get_cur_external_ip_via_google_dns, get_cur_internal_ip)
from utils_common.normalized_path import get_full_file_normal_path

BASE_DIR = Path(__file__).resolve().parent.parent

# GETTING TEST ENV CONFIGS #############################################
test_env_normal_path = get_full_file_normal_path(
    all_dir_str_parts=[BASE_DIR],
    file_name_with_ext=".env")
env = load_dotenv(test_env_normal_path)  # for future
API_TEST_USERNAME = os.getenv("API_TEST_USERNAME")
API_TEST_PASSWORD = os.getenv("API_TEST_PASSWORD")

# GETTING CURRENT INTERNAL AND EXTERNAL IPs #############################
get_cur_internal_ip(log_ip=True)
cur_external_ip = get_cur_external_ip_via_google_dns(log_ip=True)


# GETTING API INI CONFIGS ##############################################
@dataclass(frozen=True)
class API_CONFIG_NAMES:
    API_PRODUCTION = "API_production_ip"
    API_TEST = "API_test_ip"
    API_TEST_ANY_IP = "API_all_ips"
    API_TEST_WIN_LOCALHOST = "API_win_localhost"
    API_TEST_UNIX_LOCALHOST = "API_unix_localhost"


api_ini_normal_path = get_full_file_normal_path(
    all_dir_str_parts=[BASE_DIR],
    file_name_with_ext=".configs_api.ini")
api_conf_parser = ConfigParser()
api_conf_parser.read(filenames=api_ini_normal_path)

if cur_external_ip == "___.___.___.___":  # Just example
    api_conf_name = API_CONFIG_NAMES.API_TEST
elif cur_external_ip == "P.R.O.D":
    api_conf_name = API_CONFIG_NAMES.API_PRODUCTION
elif cur_external_ip == "192.168.21.22":
    api_conf_name = API_CONFIG_NAMES.API_TEST
elif sys.platform == "linux":
    api_conf_name = API_CONFIG_NAMES.API_TEST_UNIX_LOCALHOST
elif sys.platform == "win32":
    api_conf_name = API_CONFIG_NAMES.API_TEST_WIN_LOCALHOST
else:
    api_conf_name = API_CONFIG_NAMES.API_TEST_ANY_IP

API_HOST: str = api_conf_parser.get(section=api_conf_name, option="API_HOST")
API_PORT: int = int(api_conf_parser.get(section=api_conf_name, option="API_PORT"))
API_USERNAME: str = api_conf_parser.get(section=api_conf_name, option="API_USERNAME")
API_PASSWORD: str = api_conf_parser.get(section=api_conf_name, option="API_PASSWORD")
FASTAPI_SESSION_KEY: str = api_conf_parser.get(section=api_conf_name, option="FASTAPI_SESSION_KEY")


# GETTING SQLADMIN INI CONFIGS #########################################
@dataclass(frozen=True)
class SQLADMIN_CONFIG_NAMES:
    SQLADMIN_PRODUCTION = "SQLADMIN_production"
    SQLADMIN_TEST = "SQLADMIN_test"


sqladmin_ini_normal_path = get_full_file_normal_path(
    all_dir_str_parts=[BASE_DIR],
    file_name_with_ext=".configs_sqladmin.ini")
sqladmin_conf_parser = ConfigParser()
sqladmin_conf_parser.read(filenames=sqladmin_ini_normal_path)

if cur_external_ip == "___.___.___.___":  # Just example
    sqladmin_conf_name = SQLADMIN_CONFIG_NAMES.SQLADMIN_TEST
elif cur_external_ip == "P.R.O.D":
    sqladmin_conf_name = SQLADMIN_CONFIG_NAMES.SQLADMIN_PRODUCTION
elif cur_external_ip == "192.168.21.22":
    sqladmin_conf_name = SQLADMIN_CONFIG_NAMES.SQLADMIN_TEST
else:
    sqladmin_conf_name = SQLADMIN_CONFIG_NAMES.SQLADMIN_TEST

SQLADMIN_SUPERADMIN_USERNAME = sqladmin_conf_parser.get(
    section=sqladmin_conf_name, option="SQLADMIN_SUPERADMIN_USERNAME")
SQLADMIN_ADMIN_PASSWORD = sqladmin_conf_parser.get(
    section=sqladmin_conf_name, option="SQLADMIN_ADMIN_PASSWORD")
SQLADMIN_ADMIN_USERNAME = sqladmin_conf_parser.get(
    section=sqladmin_conf_name, option="SQLADMIN_ADMIN_USERNAME")
SQLADMIN_SUPERADMIN_PASSWORD = sqladmin_conf_parser.get(
    section=sqladmin_conf_name, option="SQLADMIN_SUPERADMIN_PASSWORD")


# GETTING PACT API INI CONFIGS #########################################
@dataclass(frozen=True)
class PACT_API_CONFIG_NAMES:
    PACT_API_PRODUCTION = "PACT_API_production"
    PACT_API_TEST = "PACT_API_test"


pact_api_ini_normal_path = get_full_file_normal_path(
    all_dir_str_parts=[BASE_DIR],
    file_name_with_ext=".configs_pact_api.ini")
pact_api_conf_parser = ConfigParser()
pact_api_conf_parser.read(filenames=pact_api_ini_normal_path)

if cur_external_ip == "___.___.___.___":  # Just example
    pact_api_conf_name = PACT_API_CONFIG_NAMES.PACT_API_TEST
elif cur_external_ip == "P.R.O.D":
    pact_api_conf_name = PACT_API_CONFIG_NAMES.PACT_API_PRODUCTION
if cur_external_ip == "192.168.21.22":
    pact_api_conf_name = PACT_API_CONFIG_NAMES.PACT_API_TEST
else:
    pact_api_conf_name = PACT_API_CONFIG_NAMES.PACT_API_TEST

PACT_API_TOKEN_KEY = pact_api_conf_parser.get(
    section=pact_api_conf_name, option="PACT_API_TOKEN_KEY")
PACT_API_V1_BASE_URL = pact_api_conf_parser.get(
    section=pact_api_conf_name, option="PACT_API_V1_BASE_URL")
PACT_API_V2_BASE_URL = pact_api_conf_parser.get(
    section=pact_api_conf_name, option="PACT_API_V2_BASE_URL")
PACT_EMERGENCY_CALL_URL = pact_api_conf_parser.get(
    section=pact_api_conf_name, option="PACT_EMERGENCY_CALL_URL")


# GETTING S3 MINIO INI CONFIGS ########################################
@dataclass(frozen=True)
class S3_MINIO_CONFIG_NAMES:
    S3_MINIO_PRODUCTION = "S3_MINIO_production"
    S3_MINIO_TEST = "S3_MINIO_test"


s3_minio_ini_normal_path = get_full_file_normal_path(
    all_dir_str_parts=[BASE_DIR],
    file_name_with_ext=".configs_s3_minio.ini")
s3_minio_conf_parser = ConfigParser()
s3_minio_conf_parser.read(filenames=s3_minio_ini_normal_path)

if cur_external_ip == "___.___.___.___":  # Just example
    s3_minio_conf_name = S3_MINIO_CONFIG_NAMES.S3_MINIO_TEST
elif cur_external_ip == "P.R.O.D":
    s3_minio_conf_name = S3_MINIO_CONFIG_NAMES.S3_MINIO_PRODUCTION
elif cur_external_ip == "192.168.21.22":
    s3_minio_conf_name = S3_MINIO_CONFIG_NAMES.S3_MINIO_TEST
else:
    s3_minio_conf_name = S3_MINIO_CONFIG_NAMES.S3_MINIO_TEST

S3_ENDPOINT_URL = s3_minio_conf_parser.get(
    section=s3_minio_conf_name, option="S3_ENDPOINT_URL")
S3_CONSOLE_URL = s3_minio_conf_parser.get(
    section=s3_minio_conf_name, option="S3_CONSOLE_URL")
S3_ACCESS_KEY = s3_minio_conf_parser.get(
    section=s3_minio_conf_name, option="S3_ACCESS_KEY")
S3_SECRET_KEY = s3_minio_conf_parser.get(
    section=s3_minio_conf_name, option="S3_SECRET_KEY")
S3_DEFAULT_BUCKET = s3_minio_conf_parser.get(
    section=s3_minio_conf_name, option="S3_DEFAULT_BUCKET")


# GETTING POSTGRES INI CONFIGS #########################################
@dataclass(frozen=True)
class POSTGRES_CONFIG_NAMES:
    POSTGRES_PRODUCTION = "POSTGRES_production"
    POSTGRES_TEST = "POSTGRES_test"
    POSTGRES_TEST_ANY_IP = "POSTGRES_any_ips"
    POSTGRES_TEST_WIN_LOCALHOST = "POSTGRES_win_localhost"
    POSTGRES_TEST_UNIX_LOCALHOST = "POSTGRES_unix_localhost"


postgres_ini_normal_path = get_full_file_normal_path(
    all_dir_str_parts=[BASE_DIR],
    file_name_with_ext=".configs_postgres.ini")
postgres_conf_parser = ConfigParser()
postgres_conf_parser.read(filenames=postgres_ini_normal_path)

if cur_external_ip == "___.___.___.___":  # Just example
    postgres_conf_name = POSTGRES_CONFIG_NAMES.POSTGRES_TEST
elif cur_external_ip == "P.R.O.D":
    postgres_conf_name = POSTGRES_CONFIG_NAMES.POSTGRES_PRODUCTION
elif cur_external_ip == "192.168.21.22":
    postgres_conf_name = POSTGRES_CONFIG_NAMES.POSTGRES_TEST
elif sys.platform == "linux":
    postgres_conf_name = POSTGRES_CONFIG_NAMES.POSTGRES_TEST_UNIX_LOCALHOST
elif sys.platform == "win32":
    postgres_conf_name = POSTGRES_CONFIG_NAMES.POSTGRES_TEST_WIN_LOCALHOST
else:
    postgres_conf_name = POSTGRES_CONFIG_NAMES.POSTGRES_TEST_ANY_IP

POSTGRES_USER = postgres_conf_parser.get(section=postgres_conf_name, option="POSTGRES_USER")
POSTGRES_PASSWORD = postgres_conf_parser.get(section=postgres_conf_name, option="POSTGRES_PASSWORD")
POSTGRES_HOST = postgres_conf_parser.get(section=postgres_conf_name, option="POSTGRES_HOST")
POSTGRES_PORT = postgres_conf_parser.get(section=postgres_conf_name, option="POSTGRES_PORT") or None
POSTGRES_DB_NAME = postgres_conf_parser.get(section=postgres_conf_name, option="POSTGRES_DB_NAME")


@dataclass(frozen=True)
class FASTAPI_OPTIONS:
    LOG_LEVEL = "debug"  # used in main.py when starting uvicorn
    USE_COLORS = True  # used in main.py when starting uvicorn


@dataclass(frozen=True)
class ALCHEMY_OPTIONS:
    DISABLE_SWAGGER_DOCUMENTATION: bool = True
    USE_POSTGRES_DATABASE: bool = True
    ALCHEMY_ORM_RAW_SQL_LOGS: bool = False
    ALCHEMY_QUERY_EXEC_TIME_LOGS: bool = False
    ALCHEMY_SESSION_OK_ACTIONS_LOGS: bool = False
    ALCHEMY_USE_FUTURE_ALCHEMY: bool = True
    ALCHEMY_POOL_PRE_PING: bool = True
    ALCHEMY_CONST_CONN_POOL_SIZE: int = 20
    ALCHEMY_TEMP_CONN_MAX_OVERFLOW: int = 30
    ALCHEMY_POOL_RECYCLE: int = 600  # seconds
    ALCHEMY_POOL_TIMEOUT: int = 30  # seconds


@dataclass(frozen=True)
class PACT_API_OPTIONS:
    LOG_PYDANTIC_OK_VALIDATION: bool = False
    LOG_CONVERSATION_DATA_REQ_RESPONSE: bool = False
    LOG_MESSAGE_DATA_REQ_RESPONSE: bool = False
    LOG_ALL_CONVERSATIONS_REQ_RESPONSE: bool = False
    LOG_ALL_MSGS_BY_CONVERS_REQ_RESPONSE: bool = False
    LOG_ALL_COMPANIES_REQ_RESPONSE: bool = False


@dataclass(frozen=True)
class PACT_WEBHOOKS_OPTIONS:
    WEBHOOKS_API_URL_BASE_NAME: str = "aggregator_api"
    DEBUG_SKIP_COMPANY_IDS_LIST: tuple[str] = (123456789,)  # (100179,)
    OUTGOING_EXT_API_REQ_TIMEOUT: float = 120
    LOG_WEBHOOK_INCOMING_REQ_DATA: bool = False
    LOG_WEBHOOK_INCOMING_OBJ_DATA: bool = False
    LOG_WEBHOOK_INCOMING_EXTRA_DATA: bool = False
    LOG_WEBHOOK_NEW_AUTH_DATA: bool = False
    LOG_NEW_CONVERSATION_DATA: bool = False
    LOG_NEW_MESSAGE_DATA: bool = False
    LOG_NEW_ATTACHMENT_DATA: bool = False
    MAKE_EMERGENCY_CALL: bool = False


@dataclass(frozen=True)
class PACT_SQLADMIN_OPTIONS:
    SQLADMIN_PANEL_BASE_URL: str = "/admin_panel"
    SQLADMIN_CUSTOM_TEMPLATES_DIR: str = "admin_panel/custom_templates"
    CREATE_DEFAULT_ADMIN_SUPERADMIN: bool = True
    CREATE_DEBUG_ADMIN_SUPERADMIN: bool = True
    MESSAGE_SYMBOLS_TRUNCATE_LIMIT: int = 50
    PLUS_MINUS_WORDS_TRUNCATE_LIMIT: int = 100
    CHATS_SUBJECT_TRUNCATE_LIMIT: int = 100
    # SUBJECT_CHATS_TRUNCATE_LIMIT: int = 100
    SENDER_NAME_FILTER_TRUNC_LIMIT: int = 25
    EMOJI_MAX_WIDTH: int = 500
    EMOJI_MAX_HEIGHT: int = 500
    DISPLAY_SUBJECT_AS_ARROW: bool = False


@dataclass(frozen=True)
class PACT_EMERGENCY_CALL_OPTIONS:
    EMERGENCY_CALL_URL = PACT_EMERGENCY_CALL_URL
    EMERGENCY_CALL_REQUEST_TIMEOUT: float = 120
    LOG_EMERGENCY_CALL_REQ_RESPONSE: bool = True


@dataclass(frozen=True)
class GLOBAL_API_OPTIONS:
    WEBHOOKS_GLOBAL_API_URL_BASE_NAME: str = "global_msg_aggregator"
    LOG_PYDANTIC_OK_VALIDATION: bool = False
    LOG_EXEC_TIME_GET_EACH_ATTR: bool = False  # Not used in this project yet
    LOG_NON_EXISTING_ATTR_ERROR: bool = False  # Not used in this project yet
    LOG_NON_JSONABLE_VALUE_ERROR: bool = True


@dataclass(frozen=True)
class GLOBAL_API_WEBHOOKS_OPTIONS:
    # EVENT_TYPES_SKIP_LIST: tuple[str] = ("ChatAction",)
    EVENT_TYPES_SKIP_LIST: tuple[str] = (
        # "NewMessage",
        # "MessageRead",
        # "MessageDeleted",
        # "MessageEdited",
        # "ChatAction",
        # "UserUpdate",
        # "InlineQuery",
        # "CallbackQuery",
        # "Raw",
    )
    LOG_WEBHOOK_INCOMING_REQ_DATA: bool = False
    LOG_WEBHOOK_INCOMING_OBJ_DATA: bool = False
    LOG_WEBHOOK_POSTGRES_SAVE_DATA: bool = False
    NEW_MSG_ACTION_STR: str = "new"
    EDIT_MSG_ACTION_STR: str = "edited"
    DELETE_MSG_ACTION_STR: str = "deleted"
    READ_MSG_ACTION_STR: str = "read"
    CHAT_ACTION_ACTION_STR: str = "chat action"
    USER_UPDATE_ACTION_STR: str = "user action"

    READ_EVENT_FIND_OLD_MSG_ATTEMPTS: int = 5
    READ_EVENT_FIND_OLD_MSG_DELAY_SEC: float = 1.0
    DELETED_MESSAGE_PREFIX_STR: str = "[XXX]"
    DELETED_DIFFERENCE_PART_STR: str = "(X)"
    ADDED_DIFFERENCE_PART_STR: str = "(+)"
    REPLACED_DIFFERENCE_SEPARATOR_STR: str = "(<==)"
    DIFFERENCE_EACH_LINE_SEPARATOR_STR: str = "   "

    DEFAULT_MESSAGES_CURRENT_PAGE: int = 1
    DEFAULT_MESSAGES_PER_PAGE: int = 200
