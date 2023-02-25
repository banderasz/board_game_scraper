import unittest
from unittest.mock import Mock

from Model.board_game import BoardGame, BoardGameResult
from WebScraping.error import BoardGameNotFoundError
from WebScraping.szellem_lovas_scraper import SzellemLovasScraper


class SzellemLovasTest(unittest.TestCase):
    board_game_synonym = "Spirit Island (angol) (Szellemek szigete)"
    board_game_title = "Spirit island"
    price = "39808,- Ft"
    board_game = BoardGame(board_game_title, [board_game_synonym])

    def setUp(self):
        self.driver = Mock()
        self.szellemLovasScraper = SzellemLovasScraper(self.driver)

    def test_not_founding_a_board_game_raises_error(self):
        self.driver.find_elements.return_value = []
        self.assertRaises(BoardGameNotFoundError,
                          self.szellemLovasScraper.get_board_game_results, SzellemLovasTest.board_game)

    def test_board_game_data_can_be_found(self):
        def find_elements_mock_method(*args):
            if SzellemLovasScraper.NEXT_PAGE_LOCATOR in args[1]:
                return []

            return [build_element_mock(SzellemLovasTest.price)]

        self.driver.find_elements.side_effect = find_elements_mock_method

        self.assertEqual([BoardGameResult(SzellemLovasTest.board_game_synonym, SzellemLovasTest.price)],
                         self.szellemLovasScraper.get_board_game_results(SzellemLovasTest.board_game))

    def test_board_game_data_can_be_found_on_later_page(self):
        board_games_in_pages = [[], [build_element_mock(SzellemLovasTest.price)]]

        def find_elements_mock_method(*args):
            if SzellemLovasScraper.NEXT_PAGE_LOCATOR in args[1]:
                return [Mock()] if board_games_in_pages else []

            return board_games_in_pages.pop()

        self.driver.find_elements.side_effect = find_elements_mock_method

        self.assertEqual([BoardGameResult(SzellemLovasTest.board_game_synonym, SzellemLovasTest.price)],
                         self.szellemLovasScraper.get_board_game_results(SzellemLovasTest.board_game))

    def test_boardgames_on_all_pages_are_reported(self):
        prices = ["1", "2", "3", "4"]

        board_games_in_pages = [[], [build_element_mock(prices[0])], [], [build_element_mock(prices[1])],
                                [build_element_mock(prices[2]), build_element_mock(prices[3])]]

        expected_results = [BoardGameResult(SzellemLovasTest.board_game_synonym, price) for price in prices]

        def find_elements_mock_method(*args):
            if SzellemLovasScraper.NEXT_PAGE_LOCATOR in args[1]:
                return [Mock()] if board_games_in_pages else []

            return board_games_in_pages.pop()

        self.driver.find_elements.side_effect = find_elements_mock_method

        self.assertCountEqual(expected_results,
                              self.szellemLovasScraper.get_board_game_results(SzellemLovasTest.board_game))


def build_element_mock(price: str):
    element = Mock()
    element.find_element.return_value.text = price
    return element


if __name__ == '__main__':
    unittest.main()
