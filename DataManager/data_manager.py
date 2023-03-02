import concurrent
import itertools
import logging
import threading
from collections import defaultdict
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List, Type, Dict, Callable

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from Model.board_game import BoardGame, BoardGameResult
from WebScraping.board_game_scraper import BoardGameScraper


class DataManager:
    def __init__(self, portal_scraper_classes: List[Type[BoardGameScraper]], number_of_threads: int = 1,
                 driver_generator: Callable[[], WebDriver] = None):
        self.number_of_threads = number_of_threads
        self.portal_scraper_classes = portal_scraper_classes
        self.__pool = ThreadPoolExecutor(self.number_of_threads)
        self.__driver_generator = driver_generator if driver_generator else self.__create_headless_web_driver
        self.__drivers = defaultdict(self.__driver_generator)

    @staticmethod
    def __create_headless_web_driver() -> WebDriver:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        return webdriver.Edge(options=options)

    def collect_board_game_results(self, board_games: List[BoardGame]) -> Dict[BoardGame, List[BoardGameResult]]:
        with self.__pool as executor:
            results = defaultdict(list)
            future_results = {executor.submit(self.get_board_game_results_in_portal, board_game, scraper):
                              (board_game, scraper)
                              for board_game, scraper in itertools.product(board_games, self.portal_scraper_classes)}
            for future in concurrent.futures.as_completed(future_results):
                board_game, scraper = future_results[future]
                try:
                    data = future.result()
                except Exception as exc:
                    logging.error(f"{exc} while trying to find {board_game} in {scraper}")
                else:
                    results[board_game].extend(data)
        return results

    def get_board_game_results_in_portal(self, board_game: BoardGame, scraper_class: Type[BoardGameScraper]):
        scraper = scraper_class(self.__drivers[threading.get_ident()])
        return scraper.get_board_game_results(board_game)
