from typing import Coroutine

from cherline import Cherline, Operation
from settings import Setting


async def notified_cancel_invitation_group(
    client: Cherline, op: Operation, setting: Setting
) -> Coroutine:
    """グループ招待がキャンセルされた時の処理

    Args:
        client (Cherline): Cherline Client
        op (Operation): Operation
        setting (Setting): Setting

    Returns:
        Coroutine: Coroutine
    """
    print(op)
    return await client.sendMessage(setting.ADMIN_MIDS[0], "キャンセルされた")
