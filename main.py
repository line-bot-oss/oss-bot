import asyncio
from argparse import ArgumentParser

from oss_bot import OSSBot
from settings import AppType, Environment

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

    bot = OSSBot(Environment(options.env), AppType.WINDOWS)
    bot.login_with_cherline()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run())
