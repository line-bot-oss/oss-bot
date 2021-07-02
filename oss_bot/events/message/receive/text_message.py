from typing import Coroutine

from cherline import Cherline, Operation, ToType
from settings import Setting


async def recieve_text_message(
    client: Cherline, op: Operation, setting: Setting
) -> Coroutine:
    """テキストメッセージを受け取った時の処理

    Args:
        client (Cherline): Cherline Client
        op (Operation): Operation
        setting (Setting): Setting

    Returns:
        Coroutine: Coroutine
    """
    # 送信者
    sender_mid: str = op.message.from_

    # 送信先
    to: str
    if op.message.toType in (ToType.GROUP, ToType.ROOM):
        to = op.message.to
    elif op.message.toType == ToType.USER:
        to = op.message.from_

    if op.message.text == "/mid":
        print("ok")
        return await client.sendMessage(to, sender_mid)
    return await client.sendMessage(setting.ADMIN_MIDS[0], op.message.text)
