import configparser
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
SAMPLES_DIR = ROOT_DIR / "_docs" / "msgs_aggreg_sensitive_config_samples"

INI_SAMPLE_PAIRS = [
    (
        ROOT_DIR / ".configs_api.ini",
        SAMPLES_DIR / "root_configs" / ".configs_api.ini.example",
    ),
    (
        ROOT_DIR / ".configs_pact_api.ini",
        SAMPLES_DIR / "root_configs" / ".configs_pact_api.ini.example",
    ),
    (
        ROOT_DIR / ".configs_postgres.ini",
        SAMPLES_DIR / "root_configs" / ".configs_postgres.ini.example",
    ),
    (
        ROOT_DIR / ".configs_s3_minio.ini",
        SAMPLES_DIR / "root_configs" / ".configs_s3_minio.ini.example",
    ),
    (
        ROOT_DIR / ".configs_sqladmin.ini",
        SAMPLES_DIR / "root_configs" / ".configs_sqladmin.ini.example",
    ),
]

ENV_SAMPLE_PAIRS = [
    (ROOT_DIR / ".env", SAMPLES_DIR / "root_configs" / ".env.example"),
    (
        ROOT_DIR / "docker_compose" / ".env.postgres",
        SAMPLES_DIR / "docker_compose" / ".env.postgres.example",
    ),
    (
        ROOT_DIR / "docker_compose" / ".env.s3_minio",
        SAMPLES_DIR / "docker_compose" / ".env.s3_minio.example",
    ),
]

SENSITIVE_KEY_MARKERS = (
    "PASSWORD",
    "SECRET",
    "TOKEN",
    "KEY",
    "USERNAME",
    "USER",
)


def read_ini(path: Path) -> configparser.ConfigParser:
    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser.read(path, encoding="utf-8")
    return parser


def read_env_keys(path: Path) -> list[str]:
    keys: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            continue
        key, _value = stripped_line.split("=", maxsplit=1)
        keys.append(key)
    return keys


def read_env_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            continue
        key, value = stripped_line.split("=", maxsplit=1)
        values[key] = value.strip().strip('"').strip("'")
    return values


def is_sensitive_key(key: str) -> bool:
    normalized_key = key.upper()
    return any(marker in normalized_key for marker in SENSITIVE_KEY_MARKERS)


class SensitiveConfigSamplesTest(unittest.TestCase):
    def test_ini_samples_keep_real_sections_and_keys(self) -> None:
        for real_path, sample_path in INI_SAMPLE_PAIRS:
            with self.subTest(sample=sample_path.name):
                real_config = read_ini(real_path)
                sample_config = read_ini(sample_path)

                self.assertEqual(real_config.sections(), sample_config.sections())
                for section in real_config.sections():
                    self.assertEqual(
                        list(real_config[section].keys()),
                        list(sample_config[section].keys()),
                    )

    def test_env_samples_keep_real_variable_names(self) -> None:
        for real_path, sample_path in ENV_SAMPLE_PAIRS:
            with self.subTest(sample=sample_path.name):
                self.assertEqual(read_env_keys(real_path), read_env_keys(sample_path))

    def test_samples_do_not_contain_known_real_secret_values(self) -> None:
        for real_path, sample_path in INI_SAMPLE_PAIRS:
            real_config = read_ini(real_path)
            sample_config = read_ini(sample_path)

            for section in real_config.sections():
                for key, real_value in real_config[section].items():
                    if not is_sensitive_key(key):
                        continue

                    with self.subTest(sample=sample_path.name, section=section, key=key):
                        self.assertNotEqual(
                            real_value.strip(),
                            sample_config.get(section, key).strip(),
                        )

        for real_path, sample_path in ENV_SAMPLE_PAIRS:
            real_env = read_env_values(real_path)
            sample_env = read_env_values(sample_path)

            for key, real_value in real_env.items():
                if not is_sensitive_key(key):
                    continue

                with self.subTest(sample=sample_path.name, key=key):
                    self.assertNotEqual(real_value, sample_env[key])


if __name__ == "__main__":
    unittest.main()
