from argparse import ArgumentParser

from cherline import AppType as CherlineAppType
from cherline import Cherline
from line import LINE
from settings import AppType, Environment, Setting


def login(setting: Setting) -> LINE:
    """LINEにログインする関数

    Args:
        setting (Setting): Setting

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


def login_with_cherline(client: LINE, setting: Setting) -> Cherline:
    cherline_client = Cherline(CherlineAppType[setting.app_type.name])
    cherline_client.login(client.authToken)
    return cherline_client


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage="python " + __file__ + " [--env <enviroment>] [--help]"
    )
    arg_parser.add_argument(
        "-e", "--env", help="enviroment [dev, stg, prod]", nargs="?", required=True
    )
    options = arg_parser.parse_args()

    setting = Setting(Environment(options.env), AppType.WINDOWS)
    client = login(setting)
    cherline_client = login_with_cherline(client, setting)
    print(cherline_client.token)
