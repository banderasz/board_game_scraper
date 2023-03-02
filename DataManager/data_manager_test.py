import unittest
from unittest.mock import Mock

from DataManager.data_manager import DataManager
from WebScraping.error import BoardGameNotFoundError


class DataManagerTest(unittest.TestCase):
    def setUp(self):
        self.driver = Mock()

        self.mock_scraper_class = Mock()
        self.mock_scraper = Mock()
        self.mock_scraper_class.return_value = self.mock_scraper

        self.data_manager = DataManager(driver_generator=lambda: self.driver,
                                        portal_scraper_classes=[self.mock_scraper_class])

    def test_looking_up_one_board_game_in_one_thread_works(self):
        board_game = Mock()

        self.data_manager.get_board_game_results_in_portal(board_game, self.mock_scraper_class)

        self.mock_scraper.get_board_game_results.assert_called_once_with(board_game)

    def test_looking_up_board_games_works(self):
        board_game = Mock()
        board_game_2 = Mock()

        board_game_result = Mock()
        board_game_result_2 = Mock()
        board_game_result_3 = Mock()

        def get_board_game_results_side_effect(*args):
            if args[0] == board_game:
                return [board_game_result]
            elif args[0] == board_game_2:
                return [board_game_result_2, board_game_result_3]

        self.mock_scraper.get_board_game_results.side_effect = get_board_game_results_side_effect

        result = self.data_manager.collect_board_game_results([board_game, board_game_2])

        self.assertDictEqual({board_game: [board_game_result],
                              board_game_2: [board_game_result_2, board_game_result_3]},
                             result)

    def test_getting_error_while_looking_up_board_game_not_stopping_other_reports(self):
        board_game = Mock()
        board_game_2 = Mock()

        board_game_result = Mock()

        def get_board_game_results_side_effect(*args):
            if args[0] == board_game:
                return [board_game_result]
            elif args[0] == board_game_2:
                raise BoardGameNotFoundError()

        self.mock_scraper.get_board_game_results.side_effect = get_board_game_results_side_effect

        with self.assertLogs() as captured:
            result = self.data_manager.collect_board_game_results([board_game, board_game_2])

        self.assertDictEqual({board_game: [board_game_result]}, result)
        self.assertEqual(captured.output, [f'ERROR:root:Board game is not found while trying to find {board_game_2}'
                                           f' in {self.mock_scraper_class}'])
