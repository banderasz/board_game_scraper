import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

from WebScraping.szellem_lovas_scraper import SzellemLovasScraper


class SzellemLovasTest(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Edge(options=options)
        self.szellemLovasScraper = SzellemLovasScraper(self.driver)

    def test_base_page_can_be_opened(self):
        self.szellemLovasScraper.get_base_url()
        self.assertEqual(self.driver.current_url, SzellemLovasScraper.BASE_URL)

    def test_title_can_be_searched(self):
        title = "Spirit island"
        search_result_xpath = f"//*[contains(text(), \"Keresés név alapján: '{title}'\")]"

        self.szellemLovasScraper.get_base_url()
        self.szellemLovasScraper.search_title(title)
        self.assertGreaterEqual(len(self.driver.find_elements(By.XPATH, search_result_xpath)), 1)

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
