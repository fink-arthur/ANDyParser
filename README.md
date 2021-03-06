# ANDyParser

This is a parser that will automatically generate an ANDy (Activity Network with Delay).

## How to:

This parser takes as an input a file that must follow these guidelines:

#### Entities

All the entities must be defined in one block, with a name and a decay duration for each of their level
 example:
 
lacI : [0,5,8]
tetR : [0,1,2,3,4]
cI : [0,2]
 
 
#### Potential activities 
 
The next element that needs to be defined are potential activities, we seperate them from the entities by using "%%".
They must all be defined in one block and must contain the activators, inhibitors and results as well as the duration
 example:
 
();((cI,1)) -2-> ((tetR,+1))
((lacI,2),(tetR,3));((cI,1)) -3-> ((cI,+1))
 
#### Mandatory activities
 
They are defined in the same way as the potential ones but must be separated with once again "%%"
 example:
 
();() -1-> ((tetR,+2))
((tetR,1));() -2-> ((tetR,-2))

#### Initial marking

The inital marking will define at what level each entity will begin.
It is seprated from the mandatory activities by "%%", and definied in one block
 example:
 
(tetR,1)
(cI,0)
(lacI,3)