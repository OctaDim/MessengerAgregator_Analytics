import configparser
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]


def read_ini(path: Path) -> configparser.ConfigParser:
    parser = configparser.ConfigParser()
    parser.read(path, encoding="utf-8")
    return parser


def read_env(path: Path) -> dict[str, str]:
    env_values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            continue
        key, value = stripped_line.split("=", maxsplit=1)
        env_values[key] = value
    return env_values


class LocalConfigContractTest(unittest.TestCase):
    def test_api_ini_binds_every_section_to_localhost(self) -> None:
        api_config = read_ini(ROOT_DIR / ".configs_api.ini")

        for section in api_config.sections():
            with self.subTest(section=section):
                self.assertEqual("127.0.0.1", api_config.get(section, "API_HOST"))

    def test_postgres_ini_matches_compose_localhost_publish_settings(self) -> None:
        postgres_config = read_ini(ROOT_DIR / ".configs_postgres.ini")
        postgres_env = read_env(ROOT_DIR / "docker_compose" / ".env.postgres")

        for section in postgres_config.sections():
            with self.subTest(section=section):
                self.assertEqual(
                    postgres_env["POSTGRES_USER"],
                    postgres_config.get(section, "POSTGRES_USER"),
                )
                self.assertEqual(
                    postgres_env["POSTGRES_HOST"],
                    postgres_config.get(section, "POSTGRES_HOST"),
                )
                self.assertEqual(
                    postgres_env["POSTGRES_PORT"],
                    postgres_config.get(section, "POSTGRES_PORT"),
                )
                self.assertEqual(
                    postgres_env["POSTGRES_DB_NAME"],
                    postgres_config.get(section, "POSTGRES_DB_NAME"),
                )

    def test_s3_minio_ini_matches_compose_localhost_publish_settings(self) -> None:
        s3_config = read_ini(ROOT_DIR / ".configs_s3_minio.ini")
        s3_env = read_env(ROOT_DIR / "docker_compose" / ".env.s3_minio")
        section = "S3_MINIO_localhost"

        self.assertEqual(
            f"http://{s3_env['MINIO_EXTERNAL_IP']}:{s3_env['MINIO_API_PORT']}",
            s3_config.get(section, "S3_ENDPOINT_URL"),
        )
        self.assertEqual(
            f"http://{s3_env['MINIO_EXTERNAL_IP']}:{s3_env['MINIO_CONSOLE_PORT']}",
            s3_config.get(section, "S3_CONSOLE_URL"),
        )
        self.assertEqual(
            s3_env["MINIO_DEFAULT_BUCKETS"],
            s3_config.get(section, "S3_DEFAULT_BUCKET"),
        )

    def test_pact_outbound_api_urls_are_localhost(self) -> None:
        pact_config = read_ini(ROOT_DIR / ".configs_pact_api.ini")
        section = "PACT_API_any_ip_prod"

        self.assertTrue(
            pact_config.get(section, "PACT_API_V1_BASE_URL").startswith(
                "http://127.0.0.1:"
            )
        )
        self.assertTrue(
            pact_config.get(section, "PACT_API_V2_BASE_URL").startswith(
                "http://127.0.0.1:"
            )
        )
        self.assertTrue(
            pact_config.get(section, "PACT_EMERGENCY_CALL_URL").startswith(
                "http://127.0.0.1:"
            )
        )


if __name__ == "__main__":
    unittest.main()
