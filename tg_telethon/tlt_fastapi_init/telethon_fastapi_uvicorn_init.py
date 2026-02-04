import uvicorn
from fastapi import FastAPI

from configs.settings import (
    TELETHON_FASTAPI_HOST, TELETHON_FASTAPI_PORT,
    TELETHON_FASTAPI_OPTIONS)

telethon_fastapi_app = FastAPI()

tlt_uvicorn_config = uvicorn.Config(
    app=telethon_fastapi_app,
    host=TELETHON_FASTAPI_HOST,
    port=TELETHON_FASTAPI_PORT,
    # reload=True,
    # factory=True,
    log_level=TELETHON_FASTAPI_OPTIONS.LOG_LEVEL,
    use_colors=TELETHON_FASTAPI_OPTIONS.USE_COLORS,
    loop="asyncio",  # Existing Telethon loop used
    lifespan="on", )  # Lifespan events can be used if necessary
