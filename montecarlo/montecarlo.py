import numpy as np
import pandas as pd
from random import randint
from collections import Counter

class die:
    """Die Class --TODO DELETE
    
    Creates and allows modification of a Die with N faces and W weights
    
    """
    def __init__(self, faces: np.array):
        """Initializes Die Class with user prescribed faces and initial weights of 1.0:
        
        params: 
            faces: numpy array of strings or numeric types"""
                
        # Check that faces are numpy array
        if not isinstance(faces, np.ndarray):
            raise TypeError(f'Faces must be numpy array not {type(faces)}')
            
        #TODO potentiall type check contents of array
        
        # Check that all sides are unique
        if len(faces) != len(set(faces)):
            # if not raise value error
            raise ValueError(f'Face values must be distinct. {len(faces) - len(set(faces))} are duplicated')
        
        # Create private dataframe
        self._parameters = pd.DataFrame({'face': faces})
        # Assign weights = 1
        self._parameters['weights'] = 1.0

    def change_side_weight(self, face: (int, str), weight: int):
        """Takes two arguments: the face value to be changed and the new
    weight.
        
        params:
            face: string or int value of existing face on die
            weight: new weight to be added die"""
        
        # Check that face exists before updating
        if face not in self._parameters.face.unique():
            raise IndexError(f'Invalid Face name "{face}"')
        
        # Check that weight is correct value before updating
        try:
            float(weight)
        except ValueError:
            raise TypeError(f'Invalid weight type {type(weight)}')
        
        # updates private dataframe with weight
        self._parameters.loc[self._parameters.face == face, 'weights'] = weight
        
        return self
    
    def roll_the_dice(self, rolls: int = 1):
        """Takes a parameter of how many times the die is to be rolled;
    defaults to 1. Returns a Python list of outcomes.
        
        params:
            rolls: int indicating number of rolls"""
        
        # Make sure rolls is integer and greater than 0
        if not isinstance(rolls, int) or rolls <= 0:
            raise Exception('Rolls must be integer and greater than 0')
        
        # Instantiate empty list to store results
        results = []
        
        # Roll die each time
        for roll in range(rolls):
            results.append(self._parameters.iloc[randint(0, self._parameters.shape[0]-1)])
            print(randint(0, self._parameters.shape[0]-1))
        
        # return list
        return results

    def show_die(self):
        """Shows existing state of Dice"""
 
        return self._parameters

    def __str__(self):
        """Creates REPR to type check class"""
        
        return 'Die Class'

class game:
    """Game Class
    
    Creates Game and Allows for Play by rolling dice and storing results of game play
    """
    def __init__(self, list_of_die: list):
        """Initializes Game Object from list of die
        
        params: 
            list_of_die: list containing one or more die object"""
        
        #Make sure all objects in list are Die Class
        if not all(i.__str__() == 'Die Class' for i in list_of_die):
            raise TypeError('Not all objects in list are die class')
        
        # Save to self
        self.list_of_die = list_of_die
        
    def play(self, number_of_die_rolls: int):
        """Takes an integer parameter to specify how many times the dice should
    be rolled. Saves the result of the play to a private data frame
           
        params: 
            number_of_die_rolls: int 
        
        """
        # Make sure rolls numbers are int
        if not isinstance(number_of_die_rolls, int): 
            raise TypeError(f'number_of_die_rolls must be int not {type(number_of_die_rolls)}')
        
        # save to self
        self.die_rolls = number_of_die_rolls
        
        # instantiate empty play dict
        self.play_dict = {}
        
        # roll the dice
        for enum, die in enumerate(self.list_of_die, start=1):
            # roll of each dice
            outcomes = {enum: [roll['face'] for roll in die.roll_the_dice(rolls = self.die_rolls)]}
            
            # Update Dictionary with outcomes
            self.play_dict = {**outcomes, **self.play_dict}
        
        # Create DataFrame from Dictionary of Outcomes
        self.game_results = pd.DataFrame(self.play_dict)
        # Sort by Die Num Ascending
        self.game_results = self.game_results[sorted(self.game_results.columns)]
        
        return self
        
    def most_recent_play(self, shape: str = 'wide'):
        """Shows the results of the most recent play in either wide or narrow dataframe format. Default = Wide
        
        params:
            shape: 'wide' or 'narrow'
        
        """
        # Raise Exception if incorrect parameters
        if shape.lower() not in (arg_constraints := ['narrow', 'wide']):
            raise ValueError(f'Shape not in {arg_constraints}')
        
        # If wide
        if shape == 'wide':
            # Return original game results
            return self.game_results
        
        # Otherwise it has to be narrow
        else:
            # Stack Results
            self.game_results_narrow = pd.DataFrame.from_dict(self.play_dict, orient="index").stack().to_frame(name='results')
            # Sort Index Accordingly
            self.game_results_narrow = self.game_results_narrow.swaplevel(axis=0).sort_index()
            # Return manipulated frame
            return self.game_results_narrow
        
    def __str__(self):
        """Creates REPR to type check class"""
        
        return 'Game Class'
        
class analyzer:
    """Analyzer Class
        Stores results of game play and calculates summary statistics
    """   
    def __init__(self, game):
        """Initializes Analyzer Object For Specific Game"""
        
        # check params is game class
        if game.__str__() != 'Game Class':
            
            raise ValueError(f'game should be "Game Class" not "{type(game)}"')
        
        # save to self
        self.game = game
        
    
    def jackpot(self):
        """Analyzes results to see number of times 'jackpot', or all faces being the same for rolled dices,
        happens within a specific game
        """
        # Set initially to 0
        self.num_jackpots = 0
        
        # Iterate through each play to see if jackpot happened
        for index in self.game.game_results.index:
            if len(set(self.game.game_results.iloc[index].values)) == 1:
                self.num_jackpots += 1
        
        return self.num_jackpots
    
    def face_counts_per_roll(self):
        """Computes how many times a given face is rolled in each event.

          For example, if a roll of five dice has all sixes, then the
        counts for this roll would be 5 for the face value ‘6’ and 0
        for the other faces.

         Returns a data frame of results."""
        # initializes face counts list
        face_counts = []
        # Iterates throught game results
        for index in self.game.game_results.index:
            face_counts.append(dict(self.game.game_results.iloc[index].value_counts()))
            
        # Creates dataframe of results
        self.face_counts = pd.DataFrame(face_counts)
    
        return self.face_counts
        

    def combo_counts(self):
        """Computes the distinct combinations of faces rolled, along with their
    counts.
    
        Returns a data frame of results.
        """
        # Get list to store unique combo counts
        values = []
        # Iterate through game results
        for index in self.game.game_results.index:
            values.append(tuple(set(self.game.game_results.iloc[index])))
        
        # Get count of values
        counter_results = Counter(values)
        # Create DataFrame from Values
        df = pd.DataFrame.from_dict(counter_results, orient='index').reset_index()
        # Rename column
        df = df.rename(columns={0:'count'})
        # Manual updating of dataframe
        df['index'] = df['index'].astype(str)
        df['index'] = df['index'].str.replace('(', '')
        df['index'] = df['index'].str.replace(')', '')
        # Exand index for multi-index
        df[[*range(df['index'][0].count(',')+1)]] = df['index'].str.split(',', expand=True)
        # Set Multi-Index
        df = df.set_index([i for i in df.columns if type(i) == int])
        # Drop original transforming columns
        df.drop(columns=['index'], inplace=True)
        self.combo_results = df
        return self.combo_results
    
    def permutation_counts(self):
        """Computes the distinct permutations of faces rolled, along with their
    counts.
    
        Returns a data frame of results.
        """
        
        # Create counter column
        self.game.game_results['count'] = 1
        # Group By Combos
        self.permutation_results = self.game.game_results.groupby(by=[i for i in self.game.game_results.columns if 'count' != i]).agg({'count': 'sum'})   
        
        return self.permutation_results
  

