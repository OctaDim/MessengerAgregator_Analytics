from sqladmin import action
from starlette.requests import Request
from starlette.responses import RedirectResponse

from configs.labels_messages import MESSAGES


class CanceAllFiltersSortsMixin:
    @action(
        name="cancel_filters_sorts",
        label=MESSAGES.CANCEL_ALL_FILTERS,
        confirmation_message=MESSAGES.CONFIRM_CANCEL_ALL_FILTERS,
        include_in_schema=True,
        add_in_detail=True,
        add_in_list=True)
    async def custom_action_example(
            self, request: Request,
            pks: list[str] = None  # Selected records ids strings
    ) -> RedirectResponse:
        referer_url = request.headers.get("referer")
        referer_url_no_params = referer_url.split("?")[0]
        return RedirectResponse(url=referer_url_no_params,
                                status_code=302)
