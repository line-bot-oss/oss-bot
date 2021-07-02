from typing import Coroutine

from cherline import Cherline, Operation
from settings import Setting


async def recieve_image_message(
    client: Cherline, op: Operation, setting: Setting
) -> Coroutine:
    """画像メッセージを受け取った時の処理

    Args:
        client (Cherline): Cherline Client
        op (Operation): Operation
        setting (Setting): Setting

    Returns:
        Coroutine: Coroutine
    """
    return await client.sendMessage(setting.ADMIN_MIDS[0], "画像")
