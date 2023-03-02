import unittest
import pytest

from DataManager.data_manager import DataManager

from Model.board_game import BoardGame, BoardGameResult
from WebScraping.szellem_lovas_scraper import SzellemLovasScraper


@pytest.mark.skip(reason="only for manual testing")
class DataManagerTest(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager(number_of_threads=2, portal_scraper_classes=[SzellemLovasScraper])

    def test_looking_up_board_games_works(self):
        board_game_1 = BoardGame("Ticket to Ride", ["Ticket to Ride", "Ticket to Ride: San Francisco (angol)"])
        expected_title_1 = "Ticket to Ride: San Francisco (angol)"
        expected_price_1 = "9844,- Ft"
        expected_url_1 = "https://www.szellemlovas.hu/index.php?r=webboltTermekValtozat/view&termek_valtozat_id=25474" \
                         "&uj_termek=1"

        board_game_results_1 = [BoardGameResult(expected_title_1, expected_price_1, expected_url_1)]

        board_game_2 = BoardGame("Szellemek szigete", ["Szellemek szigete"])
        expected_titles_2 = ["Spirit Island (angol) (Szellemek szigete)",
                             "Spirit Island (Szellemek szigete) - Spirit Crate"]
        expected_prices_2 = ["39808,- Ft", "18490,- Ft"]
        expected_urls_2 = ["https://www.szellemlovas.hu/index.php?r=webboltTermekValtozat/view&termek_valtozat_id=17976"
                           "&uj_termek=1",
                           "https://www.szellemlovas.hu/index.php?r=webboltTermekValtozat/view&termek_valtozat_id=25190"
                           "&uj_termek=1"]

        board_game_results_2 = [BoardGameResult(expected_title, expected_price, expected_url)
                                for expected_title, expected_price, expected_url
                                in zip(expected_titles_2, expected_prices_2, expected_urls_2)]

        result = self.data_manager.collect_board_game_results([board_game_1, board_game_2])
        self.assertDictEqual({board_game_1: board_game_results_1, board_game_2: board_game_results_2}, result)
