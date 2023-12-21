from enum import Enum


class PlayersTypes(Enum):
    """Enum class contains all the valid types of player
    """
    HUMAN = "human"
    COMPUTER_1 = "computer1"
    COMPUTER_2 = "computer2"

class ComputerLevels(Enum):
    """Enum class contains all valid computer levels
    """
    EASY = 1
    NORMAL = 2
    HARD = 3

class SelectedPlayer(Enum):
    """Class contains constants for all available options to select player from it
    """
    HUMAN = 0
    EASY_COMPUTER = 1
    NORMAL_COMPUTER = 2
    HARD_COMPUTER = 3
    UNSELECTED = -1