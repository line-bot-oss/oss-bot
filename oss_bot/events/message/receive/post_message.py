from typing import Coroutine

from cherline import Cherline, Operation
from settings import Setting
from enum import Enum


class ServiceType(Enum):
    NOTE = "NT"
    ALBUM = "AB"


async def recieve_post_message(
    client: Cherline, op: Operation, setting: Setting
) -> Coroutine:
    """投稿メッセージを受け取った時の処理

    Args:
        client (Cherline): Cherline Client
        op (Operation): Operation
        setting (Setting): Setting

    Returns:
        Coroutine: Coroutine
    """
    # 投稿者のmid
    posted_user_mid = op.message.from_
    # 投稿先（mid, gid, rid）
    posted_at = op.message.to
    # 投稿元URL
    post_url = op.message.contentMetadata["postEndUrl"]

    # サービスタイプ
    service_type = op.message.contentMetadata["serviceType"]

    # ノート
    if ServiceType[service_type] == ServiceType.NOTE:
        post_text = op.message.contentMetadata["text"]

    # アルバム
    elif ServiceType[service_type] == ServiceType.ALBUM:
        album_name = op.message.contentMetadata["albumName"]

    return await client.sendMessage(setting.ADMIN_MIDS[0], "投稿")
