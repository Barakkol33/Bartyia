from discord import Client
from discord.ext import commands

from cogs.guess_game_cog import GuessGameCog
from config import DISCORD_BOT_TOKEN_PATH


def load_discord_token() -> str:
    with open(DISCORD_BOT_TOKEN_PATH, 'r') as token_file:
        return token_file.read()


def main():
    bot = commands.Bot(command_prefix='$')

    bot.add_cog(GuessGameCog(bot))

    bot.run(load_discord_token())


if __name__ == "__main__":
    main()
