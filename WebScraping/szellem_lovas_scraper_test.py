import unittest
from collections import defaultdict
from typing import List, Dict
from unittest.mock import Mock

from Model.board_game import BoardGame, BoardGameResult
from WebScraping.error import BoardGameNotFoundError
from WebScraping.szellem_lovas_scraper import SzellemLovasScraper


class SzellemLovasTest(unittest.TestCase):
    board_game_synonym = "Spirit Island (angol) (Szellemek szigete)"
    board_game_title = "Spirit island"
    price = "39808,- Ft"
    url = "www.spirit-island.com"
    board_game = BoardGame(board_game_title, [board_game_synonym])
    board_game_result = BoardGameResult(board_game_title, price, url)

    def setUp(self):
        self.driver = Mock()
        self.szellemLovasScraper = SzellemLovasScraper(self.driver)

    def test_not_founding_a_board_game_raises_error(self):
        self.driver.find_elements.return_value = []
        self.assertRaises(BoardGameNotFoundError,
                          self.szellemLovasScraper.get_board_game_results, SzellemLovasTest.board_game)

    def test_board_game_data_can_be_found(self):
        find_boardgames_in_pages_with_driver(self.driver, [[SzellemLovasTest.board_game_result]])

        self.assertEqual([BoardGameResult(SzellemLovasTest.board_game_title, SzellemLovasTest.price,
                                          SzellemLovasTest.url)],
                         self.szellemLovasScraper.get_board_game_results(SzellemLovasTest.board_game))

    def test_board_game_data_can_be_found_on_later_page(self):
        find_boardgames_in_pages_with_driver(self.driver, [[], [self.board_game_result]])

        self.assertEqual([BoardGameResult(SzellemLovasTest.board_game_title, SzellemLovasTest.price,
                                          SzellemLovasTest.url)],
                         self.szellemLovasScraper.get_board_game_results(SzellemLovasTest.board_game))

    def test_board_games_on_all_pages_are_reported(self):
        prices = ["1", "2", "3", "4"]
        titles = ["a", "b", "c", "d"]
        urls = ["w", "x", "y", "z"]

        find_boardgames_in_pages_with_driver(self.driver, [[],
                                                           [BoardGameResult(titles[0], prices[0], urls[0])],
                                                           [],
                                                           [BoardGameResult(titles[1], prices[1], urls[1])],
                                                           [BoardGameResult(titles[2], prices[2], urls[2]),
                                                            BoardGameResult(titles[3], prices[3], urls[3])]])

        expected_results = [BoardGameResult(title, price, url) for title, price, url in zip(titles, prices, urls)]
        self.assertCountEqual(expected_results,
                              self.szellemLovasScraper.get_board_game_results(SzellemLovasTest.board_game))

    def test_multiple_results_of_synonyms_are_reported(self):
        synonym_1 = "a"
        synonym_2 = "b"
        board_game = BoardGame("title", [synonym_1, synonym_2])

        titles = ["a", "aa", "b", "bb"]
        prices = ["1", "2", "3", "4"]
        urls = ["w", "x", "y", "z"]

        use_synonyms_and_url_with_driver(self.driver,
                                         {synonym_1: [[BoardGameResult(titles[0], prices[0], urls[0]),
                                                       BoardGameResult(titles[1], prices[1], urls[1])]],
                                          synonym_2: [[BoardGameResult(titles[2], prices[2], urls[2])],
                                                      [BoardGameResult(titles[3], prices[3], urls[3])]]})

        expected_results = [BoardGameResult(title, price, url) for title, price, url in zip(titles, prices, urls)]
        self.assertCountEqual(expected_results,
                              self.szellemLovasScraper.get_board_game_results(board_game))

    def test_synonym_with_single_result_is_reported(self):
        synonym_1 = "a"
        synonym_2 = "b"
        board_game = BoardGame("title", [synonym_1, synonym_2])

        titles = ["a", "aa", "b"]
        prices = ["1", "2", "3"]
        urls = ["x", "y", "z"]

        use_synonyms_and_url_with_driver(self.driver,
                                         {synonym_1: [[BoardGameResult(titles[0], prices[0], urls[0]),
                                                       BoardGameResult(titles[1], prices[1], urls[1])]],
                                          synonym_2: [[BoardGameResult(titles[2], prices[2], urls[2])]]})

        self.assertCountEqual([BoardGameResult(titles[2], prices[2], urls[2])],
                              self.szellemLovasScraper.get_board_game_results(board_game))

    def test_if_url_is_used_if_specified(self):
        use_synonyms_and_url_with_driver(self.driver, board_game_with_url=self.board_game_result)
        url = SzellemLovasScraper.BASE_URL + "/spirit_island"

        board_game = BoardGame(self.board_game_title, [self.board_game_synonym], [url])

        self.assertEqual([BoardGameResult(self.board_game_title, self.price, url)],
                         self.szellemLovasScraper.get_board_game_results(board_game))


def use_synonyms_and_url_with_driver(driver: Mock,
                                     board_games_by_synonym: Dict[str, List[List[BoardGameResult]]] = None,
                                     board_game_with_url: BoardGameResult = None):
    if board_games_by_synonym is None:
        board_games_by_synonym = defaultdict(lambda: [[]])

    def find_element_mock_method(*args):
        mock_element = Mock()
        if args[1].endswith(SzellemLovasScraper.SEARCH_LOCATOR):
            mock_element.send_keys.side_effect = search_bar_send_keys_mock_method
        elif args[1].endswith(SzellemLovasScraper.TITLE_LOCATOR_OF_BOARD_GAME_PAGE):
            mock_element.text = board_game_with_url.title
        elif args[1].endswith(SzellemLovasScraper.PRICE_LOCATOR_OF_BOARD_GAME_PAGE):
            mock_element.text = board_game_with_url.price

        return mock_element

    def search_bar_send_keys_mock_method(*args):
        search_term = args[0][:-1]
        find_boardgames_in_pages_with_driver(driver, board_games_by_synonym[search_term])

    driver.find_element.side_effect = find_element_mock_method


def find_boardgames_in_pages_with_driver(driver: Mock, board_games_in_pages: List[List[BoardGameResult]]):
    def find_elements_mock_method(*args):
        if SzellemLovasScraper.NEXT_PAGE_LOCATOR in args[1]:
            return [Mock()] if board_games_in_pages else []

        return [build_board_game_mock(board_game_in_page) for board_game_in_page in board_games_in_pages.pop()]

    driver.find_elements.side_effect = find_elements_mock_method


def build_board_game_mock(board_game: BoardGameResult):
    board_game_box = Mock()

    def find_element_mock_method(*args):
        attribute_element = Mock()
        if args[1].endswith(SzellemLovasScraper.PRICE_LOCATOR_OF_BOARD_GAME_BOX):
            attribute_element.text = board_game.price
        elif args[1].endswith(SzellemLovasScraper.TITLE_LOCATOR_OF_BOARD_GAME_BOX):
            attribute_element.text = board_game.title
        elif args[1].endswith(SzellemLovasScraper.URL_LOCATOR_OF_BOARD_GAME_BOX):
            attribute_element.get_attribute.return_value = board_game.url
        return attribute_element

    board_game_box.find_element.side_effect = find_element_mock_method
    return board_game_box


if __name__ == '__main__':
    unittest.main()
