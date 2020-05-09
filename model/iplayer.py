from abc import ABC, abstractmethod


class IPlayer(ABC):
    @abstractmethod
    def send_personal_round(self, game_round: 'Round'):
        raise NotImplementedError()
