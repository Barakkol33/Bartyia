import random
from typing import List, Dict, Iterable

from model.iplayer import IPlayer
from model.round import Round


class GuessGameException(Exception):
    pass


class NoMoreDefinitionsException(GuessGameException):
    pass


class GuessGame(object):
    def __init__(self, definitions: Iterable[str]):
        self.__definitions: List[str] = list(definitions)

        self.__rounds: List[Round] = []

    async def start_round(self, players: List[IPlayer]) -> Round:
        game_round = Round(self.__make_definitions_by_players_map(players), len(self.__rounds))
        self.__rounds.append(game_round)

        for player in players:
            await player.send_personal_round(game_round)

        return game_round

    def get_current_round(self) -> Round:
        return self.__rounds[-1]

    def disband_current_round(self):
        current_round = self.get_current_round()

        round_definitions = current_round.definitions_by_players.values()
        self.__definitions += round_definitions

        del self.__rounds[-1]

    def __make_definitions_by_players_map(self, players: List[IPlayer]) -> Dict[IPlayer, str]:
        return {player: self.__pick_definition() for player in players}

    def __pick_definition(self) -> str:
        if not self.__definitions:
            raise NoMoreDefinitionsException()

        index = random.randint(0, len(self.__definitions) - 1)
        definition = self.__definitions[index]

        del self.__definitions[index]

        return definition
