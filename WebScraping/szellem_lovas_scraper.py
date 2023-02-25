import itertools
from typing import List, Iterable

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from Model.board_game import BoardGame, BoardGameResult
from WebScraping.error import BoardGameNotFoundError


class SzellemLovasScraper:
    BASE_URL = "https://www.szellemlovas.hu/"

    SEARCH_LOCATOR = 'header_kereses_mezo'

    BOARD_GAME_LOCATOR_BY_TITLE = '//div[contains(@class, "box-content") ' \
                                  'and .//*[contains(text(), "{title}")] ' \
                                  'and not(.//*[contains(text(), "Bontott Társasjáték")])]'

    PRICE_LOCATOR_OF_BOARD_GAME = './/div[contains(@class, "price")]'

    NEXT_PAGE_LOCATOR = '//div[contains(@class, "pager")]' \
                        '//*[contains(@class, "next") and not (contains(@class, "next hidden"))]'

    NEXT_PAGE_DISABLED_LOCATOR = '//div[contains(@class, "pager")]'

    PAGE_LIMIT = 5

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_base_url(self):
        self.driver.get(self.BASE_URL)

    def search_title(self, title: str):
        search_bar = self.driver.find_element(By.ID, SzellemLovasScraper.SEARCH_LOCATOR)
        search_bar.send_keys(title + Keys.ENTER)

    def get_board_game_results(self, board_game: BoardGame) -> List[BoardGameResult]:
        self.search_title(board_game.title)
        found_board_games = self.__find_board_games(board_game)
        if not found_board_games:
            raise BoardGameNotFoundError(f"{board_game} is not found")
        return found_board_games

    def __find_board_games(self, board_game: BoardGame) -> List[BoardGameResult]:
        return list(itertools.chain(*[board_games for board_games in self.__find_board_games_in_pages(board_game)]))

    def __find_board_games_in_pages(self, board_game: BoardGame) -> Iterable[WebElement]:
        yield self.__find_board_games_in_page(board_game)
        page_visited = 1
        while self.__try_go_to_next_page() and page_visited < SzellemLovasScraper.PAGE_LIMIT:
            page_visited += 1
            yield self.__find_board_games_in_page(board_game)

    def __try_go_to_next_page(self) -> bool:
        next_pages = self.driver.find_elements(By.XPATH, SzellemLovasScraper.NEXT_PAGE_LOCATOR)
        if len(next_pages) == 1:
            next_pages[0].click()
            return True
        return False

    def __find_board_games_in_page(self, board_game: BoardGame) -> List[BoardGameResult]:
        return list(itertools.chain(*[self.__find_board_games_by_title(title) for title in board_game.synonyms]))

    def __find_board_games_by_title(self, title: str) -> List[BoardGameResult]:
        board_games = self.driver.find_elements(By.XPATH,
                                                SzellemLovasScraper.BOARD_GAME_LOCATOR_BY_TITLE.format(title=title))
        return [self.__get_results_of_board_game(board_game, title) for board_game in board_games]

    @staticmethod
    def __get_results_of_board_game(board_game: WebElement, title: str) -> BoardGameResult:
        price = board_game.find_element(By.XPATH, SzellemLovasScraper.PRICE_LOCATOR_OF_BOARD_GAME).text
        return BoardGameResult(title, price)
