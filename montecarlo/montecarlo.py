#%%
import numpy as np
import pandas as pd
from random import randint

class die:
    
    def __init__(self, faces: np.array):
        ##TODO DOC STRING
                
        # Check that faces are numpy array
        if not isinstance(faces, np.ndarray):
            raise TypeError(f'Faces must be numpy array not {type(faces)}')
            
        #TODO potentiall type check contents of array
        
        # Check that all sides are unique
        if len(faces) != len(set(faces)):
            raise ValueError(f'Face values must be distinct. {len(faces) - len(set(faces))} are duplicated')
        
        # Create private dataframe
        self._parameters = pd.DataFrame({'face': faces})
        self._parameters['weights'] = 1.0

    def change_side_weight(self, face: (int, str), weight: int):
        ## TODO DOC STRING
        
        # Check that face exists before updating
        if face not in self._parameters.face.unique():
            raise IndexError(f'Invalid Face name "{face}"')
        
        # Check that weight is correct value before updating
        try:
            float(weight)
        except ValueError:
            raise TypeError(f'Invalid weight type {type(weight)}')
        
        self._parameters.loc[self._parameters.face == face, 'weights'] = weight
    
    def roll_the_dice(self, rolls: int = 1):
        ## TODO DOC STRING
        #TODO ADD CONSTRAINTS ON TYPE and number greater than 0
        
        results = []
        
        for roll in range(rolls):
            results.append(self._parameters.iloc[randint(0, self._parameters.shape[1]-1)])
            
        return results

    def show_die(self):
       ## TODO DOC STRING
 
        return self._parameters

    def __str__(self):
        ## TODO DOC STRING
        return 'Die Class'

class game:
    
    def __init__(self, list_of_die: list):
        #TODO make sure all die have same faces
        if not all(i.__str__() == 'Die Class' for i in list_of_die):
            raise TypeError('Not all objects in list are die class')
        
        self.list_of_die = list_of_die
        
    def play(self, number_of_die_rolls: int):
        
        # Make sure rolls numbers are int
        if not isinstance(number_of_die_rolls, int): 
            raise TypeError(f'number_of_die_rolls must be int not {type(number_of_die_rolls)}')
        
        self.die_rolls = number_of_die_rolls
        
        # instantiate empty play dict
        self.play_dict = {}
        
        # roll the dice
        for enum, die in enumerate(self.list_of_die, start=1):
            # roll of each dice
            outcomes = {enum: [roll['face'] for roll in die.roll_the_dice(rolls = self.die_rolls)]}
            
            self.play_dict = {**outcomes, **self.play_dict}
        
        self.game_results = pd.DataFrame(self.play_dict)
        self.game_results = self.game_results[sorted(self.game_results.columns)]
        
        
    def most_recent_play(self, shape: str = 'wide'):
        #TODO MAKE PIVOT OPTIONS FROM NOTES
        if shape.lower() not in (arg_constraints := ['narrow', 'wide']):
            raise ValueError(f'Shape not in {arg_constraints}')
        

        if shape == 'wide':
            
            return self.game_results
        
        else:
            self.game_results_narrow = pd.DataFrame.from_dict(self.play_dict, orient="index").stack().to_frame(name='results')
            self.game_results_narrow = self.game_results_narrow.swaplevel(axis=0).sort_index()
            return self.game_results_narrow
        
    def __str__(self):
        ## TODO DOC STRING
        return 'Game Class'
        
class analyzer:
    
    def __init__(self, game):
        ## TODO DOC STRING
        if game.__str__() != 'Game Class':
            raise ValueError(f'game should be "Game Class" not "{type(game)}"')
        
        self.game = game
        
    
    def jackpot(self):
        ## TODO DOC STRING
        self.num_jackpots = 0
        for index in self.game.game_results.index:
            if len(set(self.game.game_results.iloc[index].values)) == 1:
                self.num_jackpots += 1
                
        return self.num_jackpots
    
    def face_counts_per_roll(self):
        face_counts = []
        for index in self.game.game_results.index:
            face_counts.append(dict(self.game.game_results.iloc[index].value_counts()))
        
        self.face_counts = pd.DataFrame(face_counts)
    
        return self.face_counts
        

    def combo_counts(self):
        
        self.game.game_results['count'] = 1
        
        self.combo_results = self.game.game_results.groupby(by=[i for i in self.game.game_results.columns if 'count' != i]).agg({'count': 'sum'})   
        
        return self.combo_results
    
    
if __name__ == '__main__':
    # test it works with ints
#     tester = die(np.array([1, 2, 3]))
    # test it works with strings
    tester = die(np.array(['head', 'tails']))
    #TODO
    # test it breaks with non-numpy array
#     die([1, 2])
    # test it breaks whe face values are non-distinct
#     die(np.array([1, 2, 3, 3, 3]))

#   Test if face in list
    tester.change_side_weight('head', '2.3')
    
#   Test roll dice
#     print(tester.roll_the_dice(1))
#     print(tester.roll_the_dice(5))

# test show dice
#     print(tester.show_die())

#     print(tester.__str__() == 'Die Class')
    
# instantiate game class
    game1 = game([die(np.array([*range(20, 25)])) for _ in range(3)])
    game1.play(1000)
    print(game1.most_recent_play(shape='wide'))
    
#     game2 = game([die(np.array([1, 2])), die(np.array([2, 1]))])

# test if 
    tester2 = analyzer(game1)
    tester2.jackpot()
    tester2.face_counts_per_roll()
    print(tester2.combo_counts())