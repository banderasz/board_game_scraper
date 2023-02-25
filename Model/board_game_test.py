import unittest

from Model.board_game import BoardGame, BoardGameResult


class MyTestCase(unittest.TestCase):
    def test_board_game_and_board_game_data_representation_creates_the_original(self):
        board_game = BoardGame(title='Spirit island', synonyms=['Spirit Island'], urls=['www.spirit_island.com'])
        self.assertEqual("BoardGame(title='Spirit island', synonyms=['Spirit Island'],"
                         " urls=['www.spirit_island.com'])", repr(board_game))

        board_game_data = BoardGameResult(title='Spirit island', price='100 $', url='www.spirit_island.com')
        self.assertEqual("BoardGameData(title='Spirit island', price='100 $', url='www.spirit_island.com')",
                         repr(board_game_data))


if __name__ == '__main__':
    unittest.main()
