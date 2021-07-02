import asyncio
import traceback
from typing import Coroutine, List

from cherline import AppType as CherlineAppType
from cherline import Cherline, Operation, OpType
from line import LINE
from settings import AppType, Environment, Setting

from .op import Op
from .events.group import (
    notified_cancel_invitation_group,
    notified_invite_into_group,
)


class OSSBot(Op):
    setting: Setting
    _linepy_client: LINE
    _cherline_client: Cherline

    def __init__(self, env: Environment, app_type: AppType) -> None:
        self.setting = Setting(env, app_type)

    def login_with_linepy(self) -> None:
        """linepyでログインする関数（主にトークンが切れた時に使用）"""
        try:
            self._linepy_client = LINE(self.setting.TOKEN)
            self._linepy_client.log(
                f"Token login: {self._linepy_client.authToken}"
            )
        except Exception as _:
            self._linepy_client = LINE(
                self.setting.EMAIL,
                self.setting.PASSWORD,
                certificate=self.setting.cert_path,
                appType=self.setting.app_type.value,
            )
            self._linepy_client.log(
                f"Email login: {self._linepy_client.authToken}"
            )

        # 全友達のMID取得
        all_contact_mids = self._linepy_client.getAllContactMIDs()

        # 管理者を友達追加、起動通知
        for mid in self.setting.ADMIN_MIDS:
            if mid not in all_contact_mids:
                self._linepy_client.findAndAddContactsByMid(mid)
            self._linepy_client.sendMessage(mid, "Login success.")

        # 各環境に合った名前の変更
        self._linepy_client.profile.displayName = (
            self.setting.env.get_display_name()
        )
        self._linepy_client.updateProfile(self._linepy_client.profile)

    def login_with_cherline(self) -> None:
        """cherlineでログインする関数（Bot操作はこちらを使う）"""
        self._cherline_client = Cherline(
            CherlineAppType[self.setting.app_type.name]
        )
        self._cherline_client.login(self.setting.TOKEN)

    async def run(self) -> None:
        self._cherline_client.revision = -1
        while True:
            try:
                # fetchOps
                try:
                    ops = await self._cherline_client.fetchOps()

                except AttributeError as e:
                    traceback.print_exc()
                    continue

                revisions: List[int] = []
                op_interrput: List[Coroutine] = []

                for op in ops:
                    if op.type == OpType.END_OF_OPERATION:
                        if op.param1:
                            revision, _, _ = op.param1.partition("")
                            self._cherline_client.individualRev = int(revision)
                            self._cherline_client.globalRev = int(revision)
                    else:
                        revisions.append(op.revision)
                        op_interrput.append(self.execute(op))

                if revisions:
                    self._cherline_client.setRevisions(revisions)

                if op_interrput:
                    task = asyncio.gather(*op_interrput)
                    await task

            except Exception as _:
                traceback.print_exc()

    async def execute(self, op: Operation) -> Coroutine:
        if op.type == OpType.RECEIVE_MESSAGE:
            return await self.receive_message(op)

        elif op.type == OpType.NOTIFIED_CANCEL_INVITATION_GROUP:
            return await notified_cancel_invitation_group(*self.get_args(op))

        elif op.type == OpType.NOTIFIED_INVITE_INTO_GROUP:
            return await notified_invite_into_group(*self.get_args(op))
