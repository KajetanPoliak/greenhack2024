# greenhack2024

## Tree proposal
- fractal tree
- we need score s \in [0, 1].
- every time period (day?) we will split s branches and grow them.
- each branch has its timestamp, we prefer growing branches with lower timestamps.
- example: 
    - first day my score is 1. Therefore my tree with two branches fully grows into a bigger tree with four branches by spliting those two.
    - second day my score is 0.5, therefore I will grow only half of the tree :(

## What could be score?
- differences between import and export? Shall we condition it on the prices?
- maybe manually define rules and score evaluation? e. g. if prices are low I maybe wanna fill my battery.
- As Jan said: "this should not be our job."