from typing import Coroutine
from cherline.cherline.TalkService.ttypes import OpType, Operation
from argparse import ArgumentParser

from cherline import AppType as CherlineAppType
from cherline import Cherline
from line import LINE
from settings import AppType, Environment, Setting
import asyncio, traceback


async def execute(
    client: Cherline, op: Operation, setting: Setting
) -> Coroutine:
    print(op)
    if op.type == OpType.RECEIVE_MESSAGE:
        return await client.sendMessage(setting.ADMIN_MIDS[0], op.message.text)


def login(setting: Setting) -> LINE:
    """LINEにログインする関数

    Args:
        setting (Setting): 設定クラス

    Returns:
        LINE: LINEBot Client
    """

    try:
        client = LINE(setting.TOKEN)
        client.log(f"Token login: {client.authToken}")
    except Exception as _:
        client = LINE(
            setting.EMAIL,
            setting.PASSWORD,
            certificate=setting.cert_path,
            appType=setting.app_type.value,
        )
        client.log(f"Email login: {client.authToken}")

    # 全友達のMID取得
    all_contact_mids = client.getAllContactMIDs()

    # 管理者を友達追加、起動通知
    for mid in setting.ADMIN_MIDS:
        if mid not in all_contact_mids:
            client.findAndAddContactsByMid(mid)
        client.sendMessage(mid, "Login success.")

    # 各環境に合った名前の変更
    client.profile.displayName = setting.env.get_display_name()
    client.updateProfile(client.profile)

    return client


def login_with_cherline(setting: Setting) -> Cherline:
    """cherlineでログインする

    Args:
        client (LINE): LINEBot Client
        setting (Setting): 設定クラス

    Returns:
        Cherline: Cherlnie Client
    """
    cherline_client = Cherline(CherlineAppType[setting.app_type.name])
    cherline_client.login(setting.TOKEN)
    return cherline_client


async def run(client: Cherline, setting: Setting) -> None:
    client.revision = -1
    while True:
        try:
            try:
                ops = await client.fetchOps()
            except AttributeError as e:
                traceback.print_exc()
                continue
            revisions = []
            op_interrput: list = []
            for op in ops:
                if op.type == OpType.END_OF_OPERATION:
                    if op.param1:
                        a, _, _ = op.param1.partition("")
                        client.individualRev = int(a)
                    if op.param2:
                        a, _, _ = op.param2.partition("")
                        client.globalRev = int(a)
                else:
                    revisions.append(op.revision)

                op_interrput.append(execute(client, op, setting))

            if revisions:
                client.setRevisions(revisions)

            if op_interrput:
                task = asyncio.gather(*op_interrput)
                await task

        except Exception as _:
            traceback.print_exc()


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage="python " + __file__ + " [--env <enviroment>] [--help]"
    )
    arg_parser.add_argument(
        "-e",
        "--env",
        help="enviroment [dev, stg, prod]",
        nargs="?",
        required=True,
    )
    options = arg_parser.parse_args()

    setting = Setting(Environment(options.env), AppType.WINDOWS)
    client = login(setting)
    cherline_client = login_with_cherline(setting)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(cherline_client, setting))
