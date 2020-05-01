from typing import Dict

from discord import VoiceChannel, Member, Client
from discord.ext import commands
from discord.ext.commands import Context

from cogs.model.discord_guess_game_player import DiscordGuessGamePlayer
from config import DEFINITIONS_FILE_PATH
from model.guess_game import GuessGame, NoMoreDefinitionsException


class GuessGameCog(commands.Cog):
    LOGIN_MESSAGE = "Logged in as {}"
    MINIMUM_PLAYERS_COUNT = 2

    def __init__(self, bot: commands.Bot):
        super(GuessGameCog, self).__init__()
        self.__bot: commands.Bot = bot

        self.__definitions = self.__load_definitions()
        self.__guess_games_by_voice_channels: Dict[VoiceChannel, GuessGame] = {}

    @staticmethod
    def __load_definitions():
        with open(DEFINITIONS_FILE_PATH, 'r') as definitions_file:
            return definitions_file.readlines()

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.LOGIN_MESSAGE.format(self.__bot.user.name))

    @commands.command()
    async def new_game(self, context: Context):
        voice_channel: VoiceChannel = context.author.voice.channel
        self.__guess_games_by_voice_channels[voice_channel] = GuessGame(self.__definitions)

        await context.send(f"Created a new Guess Game for channel '{voice_channel.name}'!")

    @commands.command()
    async def start_round(self, context: Context):
        voice_channel: VoiceChannel = context.author.voice.channel
        game = self.__guess_games_by_voice_channels[voice_channel]
        players = [DiscordGuessGamePlayer(member) for member in voice_channel.members if not member.bot]

        if len(players) < self.MINIMUM_PLAYERS_COUNT:
            await context.send("Do you want to ask yourself questions? We don't have enough players in the channel...")
            return

        try:
            game_round = await game.start_round(players)
            await context.send(f"Round #{game_round.round_number} is on its way!!! Distributing the secrets... "
                               f"Everybody, check your inbox!")
        except NoMoreDefinitionsException:
            await context.send("I'm out of figures to distribute... Please start a new game!")
