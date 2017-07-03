# Artificial Intelligence Nanodegree
<a href="https://youtu.be/kmY5Y0WkchE"><img src="https://cloud.githubusercontent.com/assets/2655537/25085333/3a198a58-2327-11e7-80f5-93b4a3d5cfd8.png" width="400"></a>

## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: To solve the naked twins problem we apply the following steps:
*  From current sudoku board, we call naked_twins() to identify all naked twins grouped by unit (the complete rows, columns and 3x3 squares). 
*  In each unit, recursively remove naked twins digits from the possible value of boxes (the individual squares at the intersection of rows and columns) so that no squares outside the two naked twins squares can contain the twins values.
*  We depth first search all boxes and repeatedly apply naked twins technique to narrow the search space of possible solutions iteratively.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: To solve the diagonal sudoku problem we apply the following steps:
* Consider diagonal and reverse diagonal along with row, column, square units as part of constraints
* apply elimination strategy, only choice strategy, and naked twins technique repeatedly 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Code Review
You can find my project feedback from one of the Udacity reviewers in [here](https://review.udacity.com/#!/reviews/451359/shared)