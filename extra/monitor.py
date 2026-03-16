import aiohttp
import os


async def send_log(token: str, chat_id: str, path: str):
    if not os.path.exists(path):
        return False

    url = f"https://api.telegram.org/bot{token}/sendDocument"

    with open(path, "rb") as f:
        data = f.read()

    form = aiohttp.FormData()
    form.add_field("chat_id", chat_id)
    form.add_field("document", data, filename=os.path.basename(path))

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form) as resp:
            return resp.status == 200
