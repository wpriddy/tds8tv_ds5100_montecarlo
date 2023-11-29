
# Monte Carlo Simulator

## Author: Wyatt Priddy

### Installation

```{cmd}
# Clone the Code from the GitHub Repository
>>> git clone https://github.com/wpriddy/tds8tv_ds5100_montecarlo.git

# Change Directory into parent directory
>>> cd tds8tv_ds5100_montecarlo

# Install Package from Setup File
>>> pip install -e .
```

### Usage

```{python}
# Open python editor and import montecarlo package

>>> from montecarlo import montecarlo
>>>import numpy as np

# Create a Die Class
>>> dice = montecarlo.die(np.array(['Heads', 'Tails']))

# Create a Game Class
>>> game = montecarlo.game([dice])

# Play a Game
>>> game.play(10)

# Create Analyzer Class
>>> analyzer = montecarlo.analyzer(game)

# View Number of Times a Jackpot was Rolled
>>> analyzer.jackpot()
```

### API Description

```{text}
Die Class
    
    Creates and allows modification of a Die with N faces and corresponding W weight
      
      Methods defined here:
      
      __init__(faces: np.array)
          Initializes Die Class with user prescribed faces and initial weights of 1.0:
          
              params: 
                  faces: numpy array of strings or numeric types

          Returns self
    --------------------------------------------------------
      change_side_weight(face: ('int', 'str'), weight: int)

          Takes two arguments: the face value to be changed and the new
          weight.
              
              params:
                  face: string or int value of existing face on die
                  weight: new weight to be added die

          Returns self
    --------------------------------------------------------
      roll_the_dice(self, rolls: int = 1)
          Takes a parameter of how many times the die is to be rolled;
          defaults to 1. 
              
              params:
                  rolls: int indicating number of rolls
        
          Returns a Python list of outcomes.
      --------------------------------------------------------
      show_die()
          Shows existing state of Dice
        
          Returns Pandas.DataFrame

------------------------------------------------------------------------

 Game Class
       
    Creates Game and Allows for Play by rolling dice and storing results of game play
       
      Methods defined here:
       
      __init__(list_of_die: list)
           Initializes Game Object from list of die
           
              params: 
                  list_of_die: list containing one or more die object

           Returns self
    --------------------------------------------------------
      most_recent_play(shape: str = 'wide')
           Shows the results of the most recent play in either wide or narrow dataframe format. Default = Wide
           
              params:
                  shape: 'wide' or 'narrow'
            
           Returns Pandas.DataFrame
    --------------------------------------------------------
      play(number_of_die_rolls: int)
           Takes an integer parameter to specify how many times the dice should
           be rolled. Saves the result of the play to a private data frame
                  
              params: 
                  number_of_die_rolls: int

           Returns self
------------------------------------------------------------------------
Analyzer Class
    
    Stores results of game play and calculates summary statistics
      
      Methods defined here:
       
      __init__(game)
           Initializes Analyzer Object For Specific Game
       
           Returns self
    --------------------------------------------------------
      combo_counts()
           Computes the distinct combinations of faces rolled, along with their
           counts.
           
           Returns a data frame of results.
    --------------------------------------------------------  
      face_counts_per_roll()
           Computes how many times a given face is rolled in each event.
           
           For example, if a roll of five dice has all sixes, then the
           counts for this roll would be 5 for the face value ‘6’ and 0
           for the other faces.
           
           Returns a data frame of results.
    --------------------------------------------------------  
      jackpot()
           Analyzes results to see number of times 'jackpot', or all faces being the same for rolled dices,
           happens within a specific game

           Returns int 
    --------------------------------------------------------  
      permutation_counts()
           Computes the distinct permutations of faces rolled, along with their
           counts.
           
           Returns a data frame of results.
```
