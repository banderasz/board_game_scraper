import unittest
from typing import List
from unittest.mock import Mock

from Model.board_game import BoardGame, BoardGameResult
from WebScraping.error import BoardGameNotFoundError
from WebScraping.szellem_lovas_scraper import SzellemLovasScraper


class SzellemLovasTest(unittest.TestCase):
    board_game_synonym = "Spirit Island (angol) (Szellemek szigete)"
    board_game_title = "Spirit island"
    price = "39808,- Ft"
    board_game = BoardGame(board_game_title, [board_game_synonym])
    board_game_result = BoardGameResult(board_game_title, price)

    def setUp(self):
        self.driver = Mock()
        self.szellemLovasScraper = SzellemLovasScraper(self.driver)

    def test_not_founding_a_board_game_raises_error(self):
        self.driver.find_elements.return_value = []
        self.assertRaises(BoardGameNotFoundError,
                          self.szellemLovasScraper.get_board_game_results, SzellemLovasTest.board_game)

    def test_board_game_data_can_be_found(self):
        add_find_elements_side_effect_to_driver(self.driver, [[SzellemLovasTest.board_game_result]])

        self.assertEqual([BoardGameResult(SzellemLovasTest.board_game_title, SzellemLovasTest.price)],
                         self.szellemLovasScraper.get_board_game_results(SzellemLovasTest.board_game))

    def test_board_game_data_can_be_found_on_later_page(self):
        add_find_elements_side_effect_to_driver(self.driver, [[], [self.board_game_result]])

        self.assertEqual([BoardGameResult(SzellemLovasTest.board_game_title, SzellemLovasTest.price)],
                         self.szellemLovasScraper.get_board_game_results(SzellemLovasTest.board_game))

    def test_boardgames_on_all_pages_are_reported(self):
        prices = ["1", "2", "3", "4"]
        titles = ["a", "b", "c", "d"]

        add_find_elements_side_effect_to_driver(self.driver, [[],
                                                              [BoardGameResult(titles[0], prices[0])],
                                                              [],
                                                              [BoardGameResult(titles[1], prices[1])],
                                                              [BoardGameResult(titles[2], prices[2]),
                                                               BoardGameResult(titles[3], prices[3])]])

        expected_results = [BoardGameResult(title, price) for title, price in zip(titles, prices)]
        self.assertCountEqual(expected_results,
                              self.szellemLovasScraper.get_board_game_results(SzellemLovasTest.board_game))


def add_find_elements_side_effect_to_driver(driver: Mock, board_games_in_pages: List[List[BoardGameResult]]):
    def find_elements_mock_method(*args):
        if SzellemLovasScraper.NEXT_PAGE_LOCATOR in args[1]:
            return [Mock()] if board_games_in_pages else []

        return [build_board_game_mock(board_game_in_page) for board_game_in_page in board_games_in_pages.pop()]

    driver.find_elements.side_effect = find_elements_mock_method


def build_board_game_mock(board_game: BoardGameResult):
    board_game_box = Mock()

    def find_element_mock_method(*args):
        attribute_element = Mock()
        if SzellemLovasScraper.PRICE_LOCATOR_OF_BOARD_GAME in args[1]:
            attribute_element.text = board_game.price
        elif SzellemLovasScraper.TITLE_LOCATOR_OF_BOARD_GAME in args[1]:
            attribute_element.text = board_game.title
        return attribute_element

    board_game_box.find_element.side_effect = find_element_mock_method
    return board_game_box


if __name__ == '__main__':
    unittest.main()
