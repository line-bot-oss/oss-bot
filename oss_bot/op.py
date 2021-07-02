from typing import Coroutine, List, Union

from cherline import Cherline, ContentType, Operation, OpType
from line import LINE
from settings import Setting

from .events.message.receive.text_message import recieve_text_message
from .events.message.receive.image_message import recieve_image_message
from .events.message.receive.post_message import recieve_post_message


class Op:
    setting: Setting
    _linepy_client: LINE
    _cherline_client: Cherline

    def get_args(
        self, op: Operation
    ) -> List[Union[Cherline, Operation, Setting]]:
        return [self._cherline_client, op, self.setting]

    async def receive_message(self, op: Operation) -> Coroutine:
        # テキストメッセージ
        if (
            op.message.contentType == ContentType.NONE
            and op.message.text is not None
        ):
            return await recieve_text_message(*self.get_args(op))

        # 画像メッセージ
        elif op.message.contentType == ContentType.IMAGE:
            return await recieve_image_message(*self.get_args(op))

        # 投稿メッセージ
        elif op.message.contentType == ContentType.POSTNOTIFICATION:
            return await recieve_post_message(*self.get_args(op))

        else:
            print(
                "RECEIVE_MESSAGE: ContentType",
                ContentType._VALUES_TO_NAMES[op.message.contentType],
            )
