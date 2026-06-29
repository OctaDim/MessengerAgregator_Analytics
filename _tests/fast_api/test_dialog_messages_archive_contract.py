import os
import unittest


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(ROOT_DIR)


def read_file(file_path):
    with open(file_path, "r") as file_obj:
        return file_obj.read()


class DialogArchiveContractTests(unittest.TestCase):
    def test_main_registers_dialog_archive_router(self):
        main_source = read_file(os.path.join(PROJECT_DIR, "main.py"))
        self.assertIn("router_get_dialog_messages_archive", main_source)

    def test_router_and_query_exist(self):
        router_path = os.path.join(
            PROJECT_DIR, "fast_api", "app_get_dialog_messages_archive",
            "router_get_dialog_messages_archive.py")
        query_path = os.path.join(
            PROJECT_DIR, "db_postgres", "postgres_queries",
            "qry_get_dialog_messages_archive.py")
        self.assertTrue(os.path.exists(router_path), router_path)
        self.assertTrue(os.path.exists(query_path), query_path)

    def test_query_uses_peer_storage_mapping(self):
        query_source = read_file(os.path.join(
            PROJECT_DIR, "db_postgres", "postgres_queries",
            "qry_get_dialog_messages_archive.py"))
        self.assertIn("PEER_STORAGE_TYPE_TO_MODEL_FIELD", query_source)
        self.assertIn("ev_peer_id_user_id", query_source)
        self.assertIn("ev_peer_id_chat_id", query_source)
        self.assertIn("ev_peer_id_channel_id", query_source)


if __name__ == "__main__":
    unittest.main()

