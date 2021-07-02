import os
from enum import Enum
from os.path import join
from typing import List, Optional

from dotenv import load_dotenv


class AppType(Enum):
    ANDROID = "ANDROID"
    LINE_LITE = "ANDROIDLITE"
    IOS = "IOS"
    IPAD = "IOSIPAD"
    WINDOWS = "DESKTOPWIN"
    MAC = "DESKTOPMAC"
    CHROME = "CHROMEOS"


class DisplayName(Enum):
    DEVELOP = "OSS BOT [dev]"
    STAGING = "OSS BOT [stg]"
    PRODUCTION = "OSS BOT"


class Environment(Enum):
    DEVELOP = "dev"
    STAGING = "stg"
    PRODUCTION = "prod"

    def get_display_name(self) -> str:
        return DisplayName[self.name].value


class Setting:
    EMAIL: str
    PASSWORD: str
    TOKEN: Optional[str]
    ADMIN_MIDS: List[str] = []
    ADMIN_GIDS: List[str] = []

    env: Environment
    app_type: AppType

    def __init__(
        self, env: Environment, app_type: Optional[AppType] = None
    ) -> None:
        self.env = env
        if app_type is None:
            app_type = AppType.WINDOWS
        self.app_type = app_type

        load_dotenv(verbose=True)
        load_dotenv(self.env_path)

        self.EMAIL = os.environ["LINE_BOT_OSS_EMAIL"]
        self.PASSWORD = os.environ["LINE_BOT_OSS_PASSWORD"]
        self.TOKEN = os.environ.get("LINE_BOT_OSS_AUTH_TOKEN")

        self.__append_admin()
        self.__append_admin_gid()

    @property
    def path(self) -> str:
        """設定ディレクトリパスを返す

        Returns:
            str: 設定ディレクトリパス
        """
        return join(os.getcwd(), "line_env/oss-bot", self.env.value)

    @property
    def env_path(self) -> str:
        """環境設定ファイルのパスを返す

        Returns:
            str: 環境設定ファイルパス
        """
        return join(self.path, ".env")

    @property
    def cert_path(self) -> Optional[str]:
        """認証ファイルパスを返す

        Returns:
            Optional[str]: 認証ファイルパス
        """
        path = join(self.path, f"{self.EMAIL}.crt")
        if os.path.exists(path):
            return path
        return None

    def __append_admin(self) -> None:
        """管理者を追加する"""
        self.ADMIN_MIDS.append("u47689615351ce76d35a123c2f415faa0")

    def __append_admin_gid(self) -> None:
        """管理者用グルIDを追加する"""
        # self.ADMIN_GIDS.append("input this gid")
