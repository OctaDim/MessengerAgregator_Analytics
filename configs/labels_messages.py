from dataclasses import dataclass


@dataclass(frozen=True)
class LABELS:
    ADMIN_PANEL = "АДМИН-ПАНЕЛЬ"
    CONVERSATION = "РАЗГОВОР:"
    CONVERSATIONS = "РАЗГОВОРЫ:"
    ICON = "ℹ️"

    LOCAL_ID = "НОМЕР"
    EVENT = "СОБЫТИЕ"
    TYPE = "ТИП"
    ID = "ID"
    COMPANY_ID = "ID КОМПАНИИ"
    SENDER_NAME = "ОТПРАВИТЕЛЬ"
    SENDER_PHONE = "НОМЕР"
    SENDER_EXTERNAL_ID = "ВНЕШНИЙ НОМЕР"
    SENDER_EXTERNAL_PUBLIC_ID = "ВНЕШНИЙ ПУБЛИЧНЫЙ НОМЕР"
    PROVIDER = "ПРОВАЙДЕР"
    AVATAR_URL = "URL АВАТАРА"
    LAST_MESSAGE_ID = "ПОСЛЕДНЕЕ СООБЩЕНИЕ"
    OPERATIONAL_STATE = "СОСТОЯНИЕ"
    REPLIED_STATE = "ОТВЕЧЕННЫЙ"
    GROUP = "ГРУППОВОЙ"
    ACTIVE = "СТАТУС"
    CREATED_AT = "СОЗДАНО"
    UPDATED_AT = "ИЗМЕНЕНО"
    LOCAL_CREATED = "СОЗДАНО"
    LOCAL_UPDATED = "ИЗМЕНЕНО"

    GROUP_FILTER_TITLE = "ГРУППОВОЙ ЧАТ"
    REPLIED_FILTER_TITLE = "ОТВЕЧЕННЫЙ"
    PROVIDER_FILTER_TITLE = "ПРОВАЙДЕР"
    COMPANY_ID_FILTER_TITLE = "ID КОМПАНИИ"

    YES_FILTER_LABEL = "Да"
    NO_FILTER_LABEL = "Нет"
    ALL_RECS_FILTER_LABEL = "Все"
    REPLIED_FILTER_LABEL = "Отвеченный"
    REPLIED_FILTER_LABEL = "✅"
    UNREPLIED_FILTER_LABEL = "Неотвеченный"
    UNREPLIED_FILTER_LABEL = "❌"




@dataclass(frozen=True)
class MESSAGES:
    CANCEL_ALL_FILTERS = "СБРОСИТЬ ВСЕ ФИЛЬТРЫ И СОРТИРОВКИ"
    CONFIRM_CANCEL_ALL_FILTERS = "ОТМЕНИТЬ ВСЕ ФИЛЬТРАЦИИ И СОРТИРОВКИ ⁉️"
