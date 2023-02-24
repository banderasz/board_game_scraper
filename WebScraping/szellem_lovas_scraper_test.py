import unittest
from unittest.mock import Mock

from Model.board_game import BoardGame, BoardGameData
from WebScraping.error import BoardGameNotFoundError
from WebScraping.szellem_lovas_scraper import SzellemLovasScraper


class SzellemLovasTest(unittest.TestCase):
    def setUp(self):
        self.driver = Mock()
        self.szellemLovasScraper = SzellemLovasScraper(self.driver)

    def test_not_founding_a_board_game_raises_error(self):
        board_game = BoardGame("Spirit island", ["Spirit Island (angol) (Szellemek szigete)"])

        self.driver.find_elements.return_value = []
        self.assertRaises(BoardGameNotFoundError, self.szellemLovasScraper.get_board_game_data, board_game)

    def test_board_game_data_can_be_found(self):
        board_game = BoardGame("Spirit island", ["Spirit Island (angol) (Szellemek szigete)"])
        price = "39808,- Ft"

        element = Mock()

        self.driver.find_elements.return_value = [element]
        element.find_element.return_value.text = price

        self.assertEqual(self.szellemLovasScraper.get_board_game_data(board_game), BoardGameData(board_game, price))


if __name__ == '__main__':
    unittest.main()
