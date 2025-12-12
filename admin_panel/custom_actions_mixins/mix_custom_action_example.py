from sqladmin import action
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response


class CustomActionExampleMixin:
    @action(
        name="custom_action_example",
        label="Custom action label",
        confirmation_message="Custom confirmation message?",
        include_in_schema=True,
        add_in_detail=True,
        add_in_list=True)
    async def custom_action_example(self, request: Request,
                                    pks: list[str] = None):
        pks = request.query_params.getlist("pks")  # Selected records or directly from pks parameter
        if pks:
            # Custom functionality if selected records exist
            return RedirectResponse(
                url=request.url_for("admin:list",
                                    identity=self.identity),
                status_code=302)
        else:
            # Custom functionality if not selected records
            return Response("Action complete successfully")
