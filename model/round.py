from typing import NamedTuple, Dict

from model.iplayer import IPlayer


class Round(NamedTuple):
    definitions_by_players: Dict[IPlayer, str]
    round_number: int
