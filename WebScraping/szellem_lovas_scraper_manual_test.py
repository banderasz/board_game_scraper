import unittest

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

from Model.board_game import BoardGame, BoardGameResult
from WebScraping.szellem_lovas_scraper import SzellemLovasScraper


@pytest.mark.skip(reason="only for manual testing")
class SzellemLovasTest(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Edge(options=options)
        self.szellemLovasScraper = SzellemLovasScraper(self.driver)

    def test_base_page_can_be_opened(self):
        self.szellemLovasScraper.load_base_url()
        self.assertEqual(self.driver.current_url, SzellemLovasScraper.BASE_URL)

    def test_title_can_be_searched(self):
        title = "Spirit island"
        search_result_xpath = f"//*[contains(text(), \"Keresés név alapján: '{title}'\")]"

        self.szellemLovasScraper.load_base_url()
        self.szellemLovasScraper.search_title(title)
        self.assertGreaterEqual(len(self.driver.find_elements(By.XPATH, search_result_xpath)), 1)

    def test_board_game_data_can_be_collected_in_a_single_page(self):
        board_game = BoardGame("Spirit island", ["Spirit Island (angol) (Szellemek szigete)"])
        expected_price = "39808,- Ft"
        expected_url = "https://www.szellemlovas.hu/index.php?r=webboltTermekValtozat/view&termek_valtozat_id=17976" \
                       "&uj_termek=1"

        board_game_data = self.szellemLovasScraper.get_board_game_results(board_game)
        self.assertEqual([BoardGameResult(board_game.synonyms[0], expected_price, expected_url)], board_game_data)

    def test_board_game_data_can_be_collected_with_pagination_and_synonym(self):
        board_game = BoardGame("Ticket to Ride", ["Ticket to Ride", "Ticket to Ride: San Francisco (angol)"])
        expected_title = "Ticket to Ride: San Francisco (angol)"
        expected_price = "9844,- Ft"
        expected_url = "https://www.szellemlovas.hu/index.php?r=webboltTermekValtozat/view&termek_valtozat_id=25474" \
                       "&uj_termek=1"

        board_game_data = self.szellemLovasScraper.get_board_game_results(board_game)
        self.assertEqual([BoardGameResult(expected_title, expected_price, expected_url)], board_game_data)

    def test_multiple_board_game_results_can_be_found(self):
        board_game = BoardGame("Szellemek szigete", ["Szellemek szigete"])
        expected_titles = ["Spirit Island (angol) (Szellemek szigete)",
                           "Spirit Island (Szellemek szigete) - Spirit Crate"]
        expected_prices = ["39808,- Ft", "18490,- Ft"]
        expected_urls = ["https://www.szellemlovas.hu/index.php?r=webboltTermekValtozat/view&termek_valtozat_id=17976"
                         "&uj_termek=1",
                         "https://www.szellemlovas.hu/index.php?r=webboltTermekValtozat/view&termek_valtozat_id=25190"
                         "&uj_termek=1"]

        board_game_data = self.szellemLovasScraper.get_board_game_results(board_game)
        self.assertEqual([BoardGameResult(expected_titles[0], expected_prices[0], expected_urls[0]),
                          BoardGameResult(expected_titles[1], expected_prices[1], expected_urls[1])], board_game_data)

    def test_board_game_can_be_found_using_url(self):
        board_game = BoardGame("Szellemek szigete", ["Szellemek szigete"],
                               ["https://www.szellemlovas.hu/index.php?r=webboltTermekValtozat/view&termek_valtozat_id"
                               "=17976&uj_termek=1"])

        expected_board_game = [BoardGameResult("Spirit Island (angol) (Szellemek szigete) (Angol kiadás)", "39808,- Ft",
                                               "https://www.szellemlovas.hu/index.php?r=webboltTermekValtozat/view"
                                               "&termek_valtozat_id=17976&uj_termek=1")]

        board_game_data = self.szellemLovasScraper.get_board_game_results(board_game)
        self.assertEqual(expected_board_game, board_game_data)

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
