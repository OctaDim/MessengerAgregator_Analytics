import os
import sys
from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from utils_common.get_cur_ip_address import (
    get_cur_external_ip_via_google_dns, get_cur_internal_ip)

BASE_DIR = Path(__file__).resolve().parent.parent

# GETTING TEST ENV CONFIGS #############################################
test_env_full_path = os.path.join(BASE_DIR, ".env")
test_env_normal_path = os.path.normpath(test_env_full_path)
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


api_ini_full_path = os.path.join(BASE_DIR, ".configs_api.ini")
api_ini_normal_path = os.path.normpath(api_ini_full_path)
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


pact_api_ini_full_path = os.path.join(BASE_DIR, ".configs_pact_ext_api.ini")
pact_api_ini_normal_path = os.path.normpath(pact_api_ini_full_path)
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


fastapi_ini_full_path = os.path.join(BASE_DIR, ".configs_fastapi.ini")
fastapi_ini_normal_path = os.path.normpath(fastapi_ini_full_path)
fastapi_conf_parser = ConfigParser()
fastapi_conf_parser.read(filenames=fastapi_ini_normal_path)

if cur_external_ip == "___.___.___.___":
    fastapi_conf_name = FASTAPI_CONFIG_NAMES.FASTAPI_PRODUCT_ANY_IP  # Certain configs can be defined
else:
    fastapi_conf_name = FASTAPI_CONFIG_NAMES.FASTAPI_PRODUCT_ANY_IP

FASTAPI_SESSION_KEY = fastapi_conf_parser.get(
    section=fastapi_conf_name, option="FASTAPI_SESSION_KEY")


@dataclass(frozen=True)
class FASTAPI_OPTIONS:
    LOG_LEVEL = "debug"
    USE_COLORS = True


@dataclass(frozen=True)
class WEBHOOKS_OPTIONS:
    pass
    # # API
    # PYANNOTE_API_ROUTERS_TAG: str = "PYANNOTE_API"
    # PYANNOTE_API_REQUEST_PAUSE: int = 2
    # PYANNOTE_API_IMMEDIATE_RESPONSE: bool = True
    # LOCAL_MODEL_ROUTERS_TAG: str = "MODEL_API"
    WEBHOOKS_API_URL_BASE_NAME: str = "agregator_api"
    # TEMPORARY_AUDIO_FILE_PREFIX: str = "temp"
    # TEMPORARY_AUDIO_FILES_DIR: str = "audio_files/temporary_audio"
    # CONVERTED_AUDIO_FILES_DIR: str = "audio_files/temporary_audio"
    # CONVERTED_AUDIO_TYPE_FOR_API: str = "ogg"
    # OPERATOR_TMP_AUDIO_START_SEC: int | None = 7_000  # 7 seconds
    # OPERATOR_TMP_AUDIO_END_SEC: int | None = 60_000  # 60 seconds
    # OPERATOR_CHANNEL_SPEAKERS_NUM: int = 1
    # CALLER_TMP_AUDIO_START_SEC: int | None = 7_000  # 7 seconds
    # CALLER_TMP_AUDIO_END_SEC: int | None = 60_000  # 60 seconds
    # CALLER_CHANNEL_SPEAKERS_NUM: int = 1
    # ALL_SPEAKERS_TMP_AUDIO_START_SEC: int | None = 7_000  # 7 seconds
    # ALL_SPEAKERS_TMP_AUDIO_END_SEC: int | None = None  # 60 seconds
    # ALL_SPEAKERS_CHANNEL_SPEAKERS_NUM: int = 2
