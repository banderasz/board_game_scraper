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

        self.assertEqual([BoardGameResult(SzellemLovasTest.board_game_synonym, SzellemLovasTest.price)],
                         self.szellemLovasScraper.get_board_game_results(SzellemLovasTest.board_game))

    def test_board_game_data_can_be_found_on_later_page(self):
        add_find_elements_side_effect_to_driver(self.driver, [[], [self.board_game_result]])

        self.assertEqual([BoardGameResult(SzellemLovasTest.board_game_synonym, SzellemLovasTest.price)],
                         self.szellemLovasScraper.get_board_game_results(SzellemLovasTest.board_game))

    def test_boardgames_on_all_pages_are_reported(self):
        prices = ["1", "2", "3", "4"]

        add_find_elements_side_effect_to_driver(self.driver, [[],
                                                              [BoardGameResult("", prices[0])],
                                                              [],
                                                              [BoardGameResult("", prices[1])],
                                                              [BoardGameResult("", prices[2]),
                                                               BoardGameResult("", prices[3])]])

        expected_results = [BoardGameResult(SzellemLovasTest.board_game_synonym, price) for price in prices]

        self.assertCountEqual(expected_results,
                              self.szellemLovasScraper.get_board_game_results(SzellemLovasTest.board_game))


def add_find_elements_side_effect_to_driver(driver: Mock, board_games_in_pages: List[List[BoardGameResult]]):
    def find_elements_mock_method(*args):
        if SzellemLovasScraper.NEXT_PAGE_LOCATOR in args[1]:
            return [Mock()] if board_games_in_pages else []

        return [build_board_game_mock(board_game_in_page) for board_game_in_page in board_games_in_pages.pop()]

    driver.find_elements.side_effect = find_elements_mock_method


def build_board_game_mock(board_game: BoardGameResult):
    element = Mock()
    element.find_element.return_value.text = board_game.price
    return element


if __name__ == '__main__':
    unittest.main()
