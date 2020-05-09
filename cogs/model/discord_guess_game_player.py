from typing import Dict

from discord import Member

from model.iplayer import IPlayer
from model.round import Round


class PlayerCannotBeBotException(Exception):
    pass


class DiscordGuessGamePlayer(IPlayer):
    def __init__(self, member: Member):
        if member.bot:
            raise PlayerCannotBeBotException()

        self.__member = member

    def get_discord_member(self) -> Member:
        return self.__member

    async def send_personal_round(self, game_round: Round):
        to_send = f"The figures for Round #{game_round.round_number}:\n"

        for player, definition in game_round.definitions_by_players.items():
            if isinstance(player, DiscordGuessGamePlayer):
                if player is not self:
                    to_send += f"`{player.get_discord_member().display_name}` is `{definition}`\n"

        await self.__member.send(to_send)
