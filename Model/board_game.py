from typing import Collection


class BoardGame:
    def __init__(self, title: str, synonyms: Collection[str] = tuple()):
        self.title = title
        self.synonyms = synonyms

    def __eq__(self, other: "BoardGame"):
        return isinstance(other, BoardGame) and self.title == other.title and set(self.synonyms) == set(other.synonyms)

    def __repr__(self):
        return f"BoardGame(title='{self.title}', synonyms={self.synonyms})"


class BoardGameResult:
    def __init__(self, title: str, price: str = "", url: str = ""):
        self.title = title
        self.price = price
        self.url = url

    def __eq__(self, other: "BoardGameResult"):
        return isinstance(other, BoardGameResult) and \
               self.title == other.title and \
               self.price == other.price and \
               self.url == other.url

    def __repr__(self):
        return f"BoardGameData(title='{self.title}', price='{self.price}', url='{self.url}')"
