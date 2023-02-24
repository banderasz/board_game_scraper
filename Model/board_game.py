from typing import Collection


class BoardGame:
    def __init__(self, name: str, synonyms: Collection[str] = tuple()):
        self.name = name
        self.synonyms = synonyms

    def __eq__(self, other: "BoardGame"):
        return self.name == other.name and set(self.synonyms) == set(other.synonyms)

    def __repr__(self):
        return f"BoardGame(name='{self.name}', synonyms={self.synonyms})"


class BoardGameData:
    def __init__(self, board_game: BoardGame, price: str = ""):
        self.board_game = board_game
        self.price = price

    def __eq__(self, other: "BoardGameData"):
        return self.board_game == other.board_game and self.price == other.price

    def __repr__(self):
        return f"BoardGameData(board_game={repr(self.board_game)}, price='{self.price}')"
