from abc import ABC, abstractmethod
from typing import List

from selenium.webdriver.remote.webdriver import WebDriver

from Model.board_game import BoardGame, BoardGameResult


class BoardGameScraper(ABC):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @abstractmethod
    def get_board_game_results(self, board_game: BoardGame) -> List[BoardGameResult]:
        pass
