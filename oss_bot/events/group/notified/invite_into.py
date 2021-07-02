import asyncio
from typing import Coroutine

from cherline import Cherline, Operation
from settings import Setting


async def notified_invite_into_group(
    client: Cherline, op: Operation, setting: Setting
) -> Coroutine:
    """グループ招待された時の処理

    Args:
        client (Cherline): Cherline Client
        op (Operation): Operation
        setting (Setting): Setting

    Returns:
        Coroutine: Coroutine
    """
    # 招待されたグループのID
    invited_gid = op.param1
    # 招待した人のMID
    inviter_mid = op.param2
    # 招待された人のMID
    invitee_mid = op.param3

    await client.getProfile()
    if op.param3 == client.profile.mid:
        await client.acceptChatInvitation(invited_gid)
        return await client.sendMessage(setting.ADMIN_MIDS[0], "招待されたから入った。")
