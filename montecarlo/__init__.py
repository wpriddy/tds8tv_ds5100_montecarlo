# from montecarlo.montecarlo import die, game, analyzer
import pandas as pd
english_letters = pd.read_csv(open('data/english_letters.txt', 'r'), sep=' ', header=None)
scrabble_words = open('data/scrabble_words.txt', 'r').read().split('\n')
print(english_letters)