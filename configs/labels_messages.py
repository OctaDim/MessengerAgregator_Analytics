from dataclasses import dataclass


@dataclass(frozen=True)
class LABELS:
    ADMIN_PANEL_TITLE = "АДМИН-ПАНЕЛЬ"
    ICON = "ℹ️"

    CONVERSATION_PANEL_TITLE = "РАЗГОВОР:"
    CONVERSATIONS_PANEL_TITLE = "РАЗГОВОРЫ:"
    CONVERSATIONS_CATEGORY_TITLE = ""
    CONVERSATIONS_CATEGORY_ICON = ""

    MESSAGE_PANEL_TITLE = "СООБЩЕНИЕ:"
    MESSAGES_PANEL_TITLE = "СООБЩЕНИЯ:"
    MESSAGES_CATEGORY_TITLE = ""
    MESSAGES_CATEGORY_ICON = ""

    LOCAL_ID = "НОМЕР"
    CONVERSATION_LOCAL_ID = "ID РАЗГОВОРА"
    EVENT = "СОБЫТИЕ"
    TYPE = "ТИП"
    ID = "ID"
    EXTERNAL_ID = "ID ВНЕШНИЙ"
    CONVERSATION_ID = "ID РАЗГОВОРА"
    COMPANY_ID = "ID КОМПАНИИ"
    CONTACT_ID = "ID КОНТАКТА"
    REPLIED_TO_ID = "ID ОТВЕЧЕННОГО"
    INCOME = "ВХОДЯЩЕЕ"
    STATUS = "СТАТУС"
    MESSAGE = "СООБЩЕНИЕ"
    REACTIONS = "РЕАКЦИИ"
    DETAILS = "ДЕТАЛИ"
    ATTACHMENTS = "ВЛОЖЕНИЯ"
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
    INCOME_FILTER_TITLE = "ВХОДЯЩЕЕ"
    CONVERS_LOCAL_ID_FILTER_TITLE = "ID РАЗГОВОРА"


    YES_FILTER_LABEL = "Да"
    NO_FILTER_LABEL = "Нет"
    ALL_RECS_FILTER_LABEL = "Все"
    REPLIED_FILTER_LABEL = "☑️"  # "Отвеченный"
    UNREPLIED_FILTER_LABEL = "❌"  # "Неотвеченный"


@dataclass(frozen=True)
class MESSAGES:
    CANCEL_ALL_FILTERS = "СБРОСИТЬ ВСЕ ФИЛЬТРЫ И СОРТИРОВКИ"
    CONFIRM_CANCEL_ALL_FILTERS = "ОТМЕНИТЬ ВСЕ ФИЛЬТРАЦИИ И СОРТИРОВКИ ⁉️"
