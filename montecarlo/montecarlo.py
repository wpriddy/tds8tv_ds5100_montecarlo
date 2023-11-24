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
            results.append(randint(0, self._parameters.shape[1]-1))
            
        return results

    def show_die(self):
       ## TODO DOC STRING
 
        return self._parameters
        
        
    
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
    print(tester.roll_the_dice(1))
    print(tester.roll_the_dice(5))

# test show dice
    print(tester.show_die())

        