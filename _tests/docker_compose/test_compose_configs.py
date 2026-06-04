from pathlib import Path
import unittest


ROOT_DIR = Path(__file__).resolve().parents[2] / "docker_compose"
LOCAL_POSTGRES_COMPOSE = ROOT_DIR / "local_docker-compose_postgres.yaml"
IP_POSTGRES_COMPOSE = ROOT_DIR / "ip_docker-compose_postgres.yaml"
LOCAL_MINIO_COMPOSE = ROOT_DIR / "local_docker-compose_s3_minio.yaml"
IP_MINIO_COMPOSE = ROOT_DIR / "ip_docker-compose_s3_minio.yaml"
LOCAL_RABBITMQ_COMPOSE = ROOT_DIR / "local_docker-compose-rabbitmq_aiopika.yaml"
IP_RABBITMQ_COMPOSE = ROOT_DIR / "ip_docker-compose-rabbitmq_aiopika.yaml"
LOCAL_SSHPASS_COMPOSE = ROOT_DIR / "local_docker-compose_sshpass.yaml"
IP_SSHPASS_COMPOSE = ROOT_DIR / "ip_docker-compose_sshpass.yaml"
POSTGRES_RUNBOOK = ROOT_DIR / "POSTGRES_RUNBOOK.md"
MINIO_RUNBOOK = ROOT_DIR / "S3_MINIO_RUNBOOK.md"
RABBITMQ_RUNBOOK = ROOT_DIR / "RABBITMQ_AIOPIKA_RUNBOOK.md"
SSHPASS_RUNBOOK = ROOT_DIR / "SSHPASS_RUNBOOK.md"


class DockerComposeConfigTests(unittest.TestCase):
    def test_postgres_compose_contains_required_startup_contract(self):
        for compose_file, project_name, container_prefix in [
            (LOCAL_POSTGRES_COMPOSE, "name: octadim_local_postgres", "local"),
            (IP_POSTGRES_COMPOSE, "name: octadim_ip_postgres", "ip"),
        ]:
            text = compose_file.read_text(encoding="utf-8")

            required_fragments = [
                project_name,
                "init-postgres-dir:",
                "postgres:",
                "image: postgres:16-alpine",
                f"container_name: {container_prefix}-postgres-server-octadim",
                "condition: service_completed_successfully",
                "${POSTGRES_DATA_DIR:?err_POSTGRES_DATA_DIR_is_required}",
                "${POSTGRES_USER:?err_POSTGRES_USER_is_required}",
                "${POSTGRES_PASSWORD:?err_POSTGRES_PASSWORD_is_required}",
                "${POSTGRES_HOST:-127.0.0.1}:${POSTGRES_PORT:-5432}:5432",
                "PGDATA: /var/lib/postgresql/data/pgdata",
                "command -v psql",
                "command -v pg_isready",
                "pg_isready -h 127.0.0.1",
                "postgres_network:",
            ]

            for fragment in required_fragments:
                with self.subTest(compose_file=compose_file.name, fragment=fragment):
                    self.assertIn(fragment, text)

    def test_minio_compose_contains_required_startup_contract(self):
        for compose_file, project_name, container_prefix in [
            (LOCAL_MINIO_COMPOSE, "name: octadim_local_s3_minio", "local"),
            (IP_MINIO_COMPOSE, "name: octadim_ip_s3_minio", "ip"),
        ]:
            text = compose_file.read_text(encoding="utf-8")

            required_fragments = [
                project_name,
                "init-minio-dir:",
                "minio:",
                "create-minio-buckets:",
                "image: minio/minio:latest",
                "image: minio/mc:latest",
                f"container_name: {container_prefix}-minio-server-octadim",
                "condition: service_completed_successfully",
                "condition: service_healthy",
                "${MINIO_DATA_DIR:?err_MINIO_DATA_DIR_is_required}",
                "${MINIO_ROOT_USER:?err_MINIO_ROOT_USER_is_required}",
                "${MINIO_ROOT_PASSWORD:?err_MINIO_ROOT_PASSWORD_is_required}",
                "${MINIO_EXTERNAL_IP:-0.0.0.0}:${MINIO_API_PORT:-9000}:9000",
                "${MINIO_EXTERNAL_IP:-0.0.0.0}:${MINIO_CONSOLE_PORT:-9001}:9001",
                "mc",
                "ready",
                "local",
                "mc alias set local http://minio:9000",
                "mc mb --ignore-existing",
                "minio_network:",
            ]

            for fragment in required_fragments:
                with self.subTest(compose_file=compose_file.name, fragment=fragment):
                    self.assertIn(fragment, text)

    def test_rabbitmq_compose_contains_required_startup_contract(self):
        for compose_file, project_name, container_prefix in [
            (LOCAL_RABBITMQ_COMPOSE, "name: octadim_local_rabbitmq_aiopika", "local"),
            (IP_RABBITMQ_COMPOSE, "name: octadim_ip_rabbitmq_aiopika", "ip"),
        ]:
            text = compose_file.read_text(encoding="utf-8")

            required_fragments = [
                project_name,
                "init-rabbitmq-dir:",
                "rabbitmq:",
                "image: rabbitmq:3.13-management-alpine",
                f"container_name: {container_prefix}-rabbitmq-server-octadim-aiopika",
                "${RABBITMQ_DATA_DIR:?err_RABBITMQ_DATA_DIR_is_required}",
                "${RABBITMQ_DEFAULT_USER:?err_RABBITMQ_DEFAULT_USER_is_required}",
                "${RABBITMQ_DEFAULT_PASS:?err_RABBITMQ_DEFAULT_PASS_is_required}",
                "${RABBITMQ_ERLANG_COOKIE:?err_RABBITMQ_ERLANG_COOKIE_is_required}",
                "${RABBITMQ_EXTERNAL_IP:-127.0.0.1}:${RABBITMQ_AMQP_PORT:-5672}:5672",
                "${RABBITMQ_EXTERNAL_IP:-127.0.0.1}:${RABBITMQ_MANAGEMENT_PORT:-15672}:15672",
                "rabbitmq-diagnostics -q ping",
                "rabbitmq_aiopika_network:",
            ]

            for fragment in required_fragments:
                with self.subTest(compose_file=compose_file.name, fragment=fragment):
                    self.assertIn(fragment, text)

    def test_sshpass_compose_contains_required_startup_contract(self):
        for compose_file, project_name, container_prefix in [
            (LOCAL_SSHPASS_COMPOSE, "name: octadim_local_sshpass", "local"),
            (IP_SSHPASS_COMPOSE, "name: octadim_ip_sshpass", "ip"),
        ]:
            text = compose_file.read_text(encoding="utf-8")

            required_fragments = [
                project_name,
                "sshpass-tools:",
                "image: alpine:3.20",
                f"container_name: {container_prefix}-sshpass-tools-octadim",
                "apk add --no-cache openssh-client sshpass",
                "command -v sshpass",
                "command -v ssh",
                "sshpass -V",
            ]

            for fragment in required_fragments:
                with self.subTest(compose_file=compose_file.name, fragment=fragment):
                    self.assertIn(fragment, text)

    def test_runbooks_reference_expected_env_files_and_validation_commands(self):
        postgres_text = POSTGRES_RUNBOOK.read_text(encoding="utf-8")
        minio_text = MINIO_RUNBOOK.read_text(encoding="utf-8")
        rabbitmq_text = RABBITMQ_RUNBOOK.read_text(encoding="utf-8")
        sshpass_text = SSHPASS_RUNBOOK.read_text(encoding="utf-8")

        self.assertIn("--env-file .env_local_postgres", postgres_text)
        self.assertIn("--env-file .env.ip_postgres", postgres_text)
        self.assertIn("docker-compose -f local_docker-compose_postgres.yaml", postgres_text)
        self.assertIn("docker-compose -f ip_docker-compose_postgres.yaml", postgres_text)
        self.assertIn("config --quiet", postgres_text)

        self.assertIn("--env-file .env_local_s3_minio", minio_text)
        self.assertIn("--env-file .env.ip_s3_minio", minio_text)
        self.assertIn("docker-compose -f local_docker-compose_s3_minio.yaml", minio_text)
        self.assertIn("docker-compose -f ip_docker-compose_s3_minio.yaml", minio_text)
        self.assertIn("config --quiet", minio_text)

        self.assertIn("--env-file .env_local_rabbitmq_aiopika", rabbitmq_text)
        self.assertIn("--env-file .env.ip_rabbitmq_aiopika", rabbitmq_text)
        self.assertIn("docker-compose -f local_docker-compose-rabbitmq_aiopika.yaml", rabbitmq_text)
        self.assertIn("docker-compose -f ip_docker-compose-rabbitmq_aiopika.yaml", rabbitmq_text)
        self.assertIn("config --quiet", rabbitmq_text)

        self.assertIn("docker-compose -f local_docker-compose_sshpass.yaml", sshpass_text)
        self.assertIn("docker-compose -f ip_docker-compose_sshpass.yaml", sshpass_text)
        self.assertIn("config --quiet", sshpass_text)


if __name__ == "__main__":
    unittest.main()
