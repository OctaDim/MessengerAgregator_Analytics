import importlib
import sys
import types
import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException


class FakeAsyncConnection:
    def __init__(self):
        self.engine = object()


class FakeAsyncSession:
    def __init__(self, engine=None, log_good_ops=False):
        self.engine = engine
        self.log_good_ops = log_good_ops

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class TestMessagesByContactsRouter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        fake_ip_module = types.ModuleType("utils_common.get_cur_ip_address")
        fake_ip_module.get_cur_external_ip_via_google_dns = (
            lambda log_ip=True: "127.0.0.1")
        fake_ip_module.get_cur_internal_ip = lambda log_ip=True: "127.0.0.1"

        cls.ip_module_patch = patch.dict(
            sys.modules,
            {"utils_common.get_cur_ip_address": fake_ip_module})
        cls.ip_module_patch.start()
        cls.router_module = importlib.import_module(
            "fast_api.app_get_paginated_messages_by_contacts."
            "router_get_messages_by_contacts")
        cls.scheme_module = importlib.import_module(
            "fast_api.app_get_paginated_messages_by_contacts."
            "scheme_messages_by_contacts")

    @classmethod
    def tearDownClass(cls):
        cls.ip_module_patch.stop()

    def setUp(self):
        self.auth_data = self.router_module.AuthData(
            username="api_user",
            password="api_password")
        self.web_account_data = self.router_module.InWebAccountData(
            web_account_id="501",
            web_account_username="manager_account")

    def test_get_messages_by_contacts_router_success(self):
        response_data = {
            "paginated_messages": [
                {
                    "id": 101,
                    "username_cst": "contact_1",
                    "phone_cst": "+10000000001",
                    "tlt_config_name": "telethon_cfg_1",
                }
            ],
            "all_messages_count": 1,
        }
        pagination_data = self.router_module.InMessagesByContactsPagination(
            current_page=1,
            messages_per_page=25,
            tlt_config_name="telethon_cfg_1",
            telegram_contacts=[
                self.scheme_module.InTelegramContactData(
                    username_cst="contact_1")
            ])

        with patch.object(
                self.router_module,
                "verify_auth_username_password",
                new=AsyncMock(return_value=True)), \
                patch.object(
                    self.router_module,
                    "PgsAsyncConnection",
                    new=FakeAsyncConnection), \
                patch.object(
                    self.router_module,
                    "PgsAsyncSession",
                    new=FakeAsyncSession), \
                patch.object(
                    self.router_module,
                    "get_paginated_messages_by_contacts_qry",
                    new=AsyncMock(return_value=response_data)):
            response = asyncio.run(
                self.router_module.get_messages_by_contacts_list_router(
                    auth_data=self.auth_data,
                    web_account_data=self.web_account_data,
                    pagination_data=pagination_data))

        self.assertEqual(response.status_code, 200)
        response_json = response.body.decode("utf-8")
        self.assertIn('"all_msgs_count":1', response_json)
        self.assertIn('"paginated_msgs_count":1', response_json)
        self.assertIn('"tlt_config_name":"telethon_cfg_1"', response_json)
        self.assertIn('"username_cst":"contact_1"', response_json)

    def test_get_messages_by_contacts_router_rejects_empty_contacts(self):
        with self.assertRaises(HTTPException) as raised_error:
            self.router_module.InMessagesByContactsPagination(
                current_page=1,
                messages_per_page=25,
                telegram_contacts=[])

        self.assertEqual(raised_error.exception.status_code, 400)
        self.assertIn("Empty telegram contacts list",
                      raised_error.exception.detail)


if __name__ == "__main__":
    unittest.main()
