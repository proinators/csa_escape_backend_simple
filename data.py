from enum import Enum

class GameStatus(Enum):
    """The game status. The scene shown on the game."""
    idle=0
    snitch=1
    minesweeper=2

class DisplayStatus(Enum):
    """The display status. The scene shown on the display thing."""
    idle=0
    timer=1
    gameover=2

class DisplayEvent(Enum):
    victory = "victory"
    fail = "fail"

class MusicPlaylist(Enum):
    """The MusicPlaylist being played (for admin control)"""
    reset=0
    intro=1
    game=2
    end=3


class Data:
    """The main data object of the server, where the server state, clue list and quiz questions are stored."""
    status = GameStatus.idle
    display = DisplayStatus.idle
