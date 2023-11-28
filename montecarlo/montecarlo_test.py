from montecarlo import die, game, analyzer
import unittest
import numpy as np
import pandas as pd

# Initialize a Die
test_die = die(np.array(['heads', 'tails']))

# Initialize a Game
test_game = game([test_die, test_die])

# Initialize the Analyzer
test_analyzer = analyzer(test_game.play(10))

class montecarlo_test_suite(unittest.TestCase):
    
    def test_die_initializer(self):
        # Test that initializing die class creates private pd.DataFrame
        self.assertEqual(type(test_die._parameters), pd.DataFrame)

    def test_die_change_side_weight(self):
        # Test that changing the side weight updates correctly
        test_die.change_side_weight('heads', 33)
        
        self.assertTrue(test_die._parameters[test_die._parameters.face == 'heads']['weights'][0] == 33, 'Face weight did not update')
        
    def test_die_roll_output(self):
        # Test die roll outputs list
        self.assertEqual(type(test_die.roll_the_dice(3)), list, "Dice Roll did not return list")
    
    def test_die_show_the_dice(self):
        #Test that show the dice returns pd.DataFrame
        self.assertEqual(type(test_die.show_die()), pd.DataFrame, 'Show Dice did not return pandas DataFrame')
    
    def test_game_initializer(self):
        # Test that initializer stores list of die
        self.assertEqual(test_game.list_of_die, [test_die, test_die], 'Game initializer did not store die')
    
    def test_game_play(self):
        # test game play saves results to pd.DataFrame
        test_game.play(3)
        self.assertIsInstance(test_game.game_results, pd.DataFrame, 'Game results are not pandas DataFrame')
    
    def test_game_results_narrow(self):
        # Test that narrow dataframe return only 1 column
        self.assertTrue(len(test_game.most_recent_play(shape='narrow').columns) == 1, 'Narrow function returned more than one column')
    
    def test_analyzer_initializer(self):
        # Test that the analyzer won't initialize without a game object
        self.assertRaises(ValueError, analyzer, "won't work")
        
    def test_analyzer_jackpot(self):
        # Test that jackpot returns an int
        self.assertIsInstance(test_analyzer.jackpot(), int, 'Jackpot is not integer')

    def test_analyzer_face_counts_per_roll(self):
        #Test that Face Counts returns pd.DataFrame
        self.assertIsInstance(test_analyzer.face_counts_per_roll(), pd.DataFrame, 'Face counts is not pd.DataFrame')
    
    def test_analyzer_combo_counts(self):
        #Test that Combo Counts returns pd.DataFrame with multi-index
        self.assertIsInstance(test_analyzer.combo_counts().index, pd.core.indexes.multi.MultiIndex, 'Combo Counts is not multi-index pd.DataFrame')     
    
    def test_analyzer_permutation_counts(self):
        #Test that Permutation Counts returns pd.DataFrame with multi-index
        self.assertIsInstance(test_analyzer.permutation_counts().index, pd.core.indexes.multi.MultiIndex, 'Combo Counts is not multi-index pd.DataFrame')     
        
if __name__ == '__main__':
    unittest.main(verbosity=3)
