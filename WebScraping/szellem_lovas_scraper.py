from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from Model.board_game import BoardGame, BoardGameData
from WebScraping.error import BoardGameNotFoundError


class SzellemLovasScraper:
    BASE_URL = "https://www.szellemlovas.hu/"

    SEARCH_LOCATOR = 'header_kereses_mezo'

    BOARD_GAME_LOCATOR_BY_TITLE = '//div[contains(@class, "box-content") ' \
                                  'and .//*[contains(text(), "{title}")] ' \
                                  'and not(.//*[contains(text(), "Bontott Társasjáték")])]'

    PRICE_LOCATOR_OF_BOARD_GAME = './/div[contains(@class, "price")]'

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_base_url(self):
        self.driver.get(self.BASE_URL)

    def search_title(self, title: str):
        search_bar = self.driver.find_element(By.ID, SzellemLovasScraper.SEARCH_LOCATOR)
        search_bar.send_keys(title + Keys.ENTER)

    def get_board_game_data(self, board_game: BoardGame) -> BoardGameData:
        self.search_title(board_game.name)
        found_board_game = self.__find_correct_board_game(board_game)
        if not found_board_game:
            raise BoardGameNotFoundError(f"{board_game} is not found")
        price = found_board_game.find_element(By.XPATH, SzellemLovasScraper.PRICE_LOCATOR_OF_BOARD_GAME).text
        return BoardGameData(board_game, price)

    def __find_correct_board_game(self, board_game: BoardGame) -> WebElement:
        for synonym in [board_game.name, *board_game.synonyms]:
            elements = self.driver.find_elements(By.XPATH,
                                                 SzellemLovasScraper.BOARD_GAME_LOCATOR_BY_TITLE.format(title=synonym))
            if len(elements) == 1:
                return elements[0]
