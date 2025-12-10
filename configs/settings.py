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
    API_PRODUCT_SERVER_IP = "API_production"
    API_HAKASIA_PROD_SERVER_IP = "API_Hakasia_product_server"
    API_TEST_176_124_136_22_IP = "API_test_server_176_124_136_22_8000"
    API_TEST_192_168_21_22_IP = "API_test_server_192_168_21_22_8000"
    API_TEST_PORT_ANY_IP = "API_port_all_ips_0_0_0_0_8000"
    API_TEST_WIN_LOCALHOST = "API_win_localhost_127_0_0_1_8000"
    API_TEST_UNIX_LOCALHOST = "API_unix_localhost_127_0_1_1_8000"
    API_TEST_DEXP_1_IP = "API_dexp_ip_192_168_0_117_8000"
    API_TEST_DEXP_2_IP = "API_dexp_ip_192_168_0_106_8000"


api_ini_normal_path = get_full_file_normal_path(
    all_dir_str_parts=[BASE_DIR],
    file_name_with_ext=".configs_api.ini")
api_conf_parser = ConfigParser()
api_conf_parser.read(filenames=api_ini_normal_path)

if cur_external_ip == "___.___.___.___":  # Just example
    api_conf_name = API_CONFIG_NAMES.API_TEST_PORT_ANY_IP
elif cur_external_ip == "172.19.201.24":
    api_conf_name = API_CONFIG_NAMES.API_PRODUCT_SERVER_IP
elif cur_external_ip == "172.19.201.24":
    api_conf_name = API_CONFIG_NAMES.API_HAKASIA_PROD_SERVER_IP
elif cur_external_ip == "176.124.136.22":
    api_conf_name = API_CONFIG_NAMES.API_TEST_176_124_136_22_IP
elif cur_external_ip == "192.168.21.22":
    api_conf_name = API_CONFIG_NAMES.API_TEST_192_168_21_22_IP
elif cur_external_ip == "192.168.0.117":
    api_conf_name = API_CONFIG_NAMES.API_TEST_DEXP_1_IP
elif cur_external_ip == "192.168.0.106":
    api_conf_name = API_CONFIG_NAMES.API_TEST_DEXP_2_IP
elif sys.platform == "linux":
    api_conf_name = API_CONFIG_NAMES.API_TEST_UNIX_LOCALHOST
elif sys.platform == "win32":
    api_conf_name = API_CONFIG_NAMES.API_TEST_WIN_LOCALHOST
else:
    api_conf_name = API_CONFIG_NAMES.API_TEST_PORT_ANY_IP

API_HOST: str = api_conf_parser.get(section=api_conf_name, option="API_HOST")
API_PORT: int = int(api_conf_parser.get(section=api_conf_name, option="API_PORT"))
API_USERNAME: str = api_conf_parser.get(section=api_conf_name, option="API_USERNAME")
API_PASSWORD: str = api_conf_parser.get(section=api_conf_name, option="API_PASSWORD")


# GETTING PACT API INI CONFIGS ##############################################
@dataclass(frozen=True)
class PACT_API_CONFIG_NAMES:
    PACT_API_ANY_PRODUCT_IP = "PACT_API_any_ip_prod"


pact_api_ini_normal_path = get_full_file_normal_path(
    all_dir_str_parts=[BASE_DIR],
    file_name_with_ext=".configs_pact_ext_api.ini")
pact_api_conf_parser = ConfigParser()
pact_api_conf_parser.read(filenames=pact_api_ini_normal_path)

if cur_external_ip == "___.___.___.___":  # Just example
    pact_api_conf_name = PACT_API_CONFIG_NAMES.PACT_API_ANY_PRODUCT_IP  # Certain configs can be defined
else:
    pact_api_conf_name = PACT_API_CONFIG_NAMES.PACT_API_ANY_PRODUCT_IP

PACT_API_TOKEN_KEY = pact_api_conf_parser.get(
    section=pact_api_conf_name, option="PACT_API_TOKEN_KEY")


# GETTING FASTAPI INI CONFIGS #########################################
@dataclass(frozen=True)
class FASTAPI_CONFIG_NAMES:
    FASTAPI_PRODUCT_ANY_IP = "FastAPI_any_ip_prod_configs"


fastapi_ini_normal_path = get_full_file_normal_path(
    all_dir_str_parts=[BASE_DIR],
    file_name_with_ext=".configs_fastapi.ini")
fastapi_conf_parser = ConfigParser()
fastapi_conf_parser.read(filenames=fastapi_ini_normal_path)

if cur_external_ip == "___.___.___.___":
    fastapi_conf_name = FASTAPI_CONFIG_NAMES.FASTAPI_PRODUCT_ANY_IP  # Certain configs can be defined
else:
    fastapi_conf_name = FASTAPI_CONFIG_NAMES.FASTAPI_PRODUCT_ANY_IP

FASTAPI_SESSION_KEY = fastapi_conf_parser.get(
    section=fastapi_conf_name, option="FASTAPI_SESSION_KEY")


# GETTING POSTGRES INI CONFIGS #########################################
@dataclass(frozen=True)
class POSTGRES_CONFIG_NAMES:
    POSTGRES_PRODUCT_SERVER_IP = "Postgres_production"
    POSTGRES_HAKASIA_PROD_SERVER_IP = "Postgres_Hakasia_product_server"
    POSTGRES_TEST_176_124_136_22_IP = "Postgres_prod_server_176_124_136_22"
    POSTGRES_TEST_PORT_ANY_IP = "Postgres_port_all_ips_0_0_0_0_8000"
    POSTGRES_TEST_WIN_LOCALHOST = "Postgres_win_localhost_127_0_0_1_8000"
    POSTGRES_TEST_UNIX_LOCALHOST = "Postgres_unix_localhost_127_0_1_1_8000"
    POSTGRES_TEST_DEXP_IP = "Postgres_dexp_ip_192_168_0_117_8000"


postgres_ini_normal_path = get_full_file_normal_path(
    all_dir_str_parts=[BASE_DIR],
    file_name_with_ext=".configs_postgres.ini")
postgres_conf_parser = ConfigParser()
postgres_conf_parser.read(filenames=postgres_ini_normal_path)

if cur_external_ip == "___.___.___.___":  # Just example
    postgres_conf_name = POSTGRES_CONFIG_NAMES.POSTGRES_TEST_PORT_ANY_IP
elif cur_external_ip == "172.19.201.24":
    postgres_conf_name = POSTGRES_CONFIG_NAMES.POSTGRES_PRODUCT_SERVER_IP
elif cur_external_ip == "172.19.201.24":
    postgres_conf_name = POSTGRES_CONFIG_NAMES.POSTGRES_HAKASIA_PROD_SERVER_IP
elif cur_external_ip == "176.124.136.22":
    postgres_conf_name = POSTGRES_CONFIG_NAMES.POSTGRES_TEST_176_124_136_22_IP
elif cur_external_ip == "192.168.0.117":
    postgres_conf_name = POSTGRES_CONFIG_NAMES.POSTGRES_TEST_DEXP_IP
elif sys.platform == "linux":
    postgres_conf_name = POSTGRES_CONFIG_NAMES.POSTGRES_TEST_UNIX_LOCALHOST
elif sys.platform == "win32":
    postgres_conf_name = POSTGRES_CONFIG_NAMES.POSTGRES_TEST_WIN_LOCALHOST
else:
    postgres_conf_name = POSTGRES_CONFIG_NAMES.POSTGRES_TEST_PORT_ANY_IP

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
class API_OPTIONS:
    LOG_PYDANTIC_OK_VALIDATION: bool = False


@dataclass(frozen=True)
class WEBHOOKS_OPTIONS:
    WEBHOOKS_API_URL_BASE_NAME: str = "aggregator_api"
    OUTGOING_EXT_API_REQUEST_TIMEOUT: float = 120
    LOG_WEBHOOK_INCOMING_REQ_DATA: bool = False
    LOG_WEBHOOK_INCOMING_OBJ_DATA: bool = False
    LOG_WEBHOOK_INCOMING_EXTRA_DATA: bool = False
