# ANDyParser

This is a parser that will automatically generate an ANDy (Activity Network with Delay).

## How to:

This parser takes as an input a file, that must follow these guidelines:

#### Entities

All the entities must be defined in one block, with a name and a decay duration for each of their level
 \nexample:\n
 
lacI : [0,5,8]\n
tetR : [0,1,2,3,4]\n
cI : [0,2]\n
 
 
#### Potential activities 
 
The next element that needs to be defined are potential activities, we seperate them from the entities by using "%%".
They must all be defined in one block and must contain the activators, inhibitors adn results as well as the duration
 \nexample:\n
 
();((cI,1)) -2-> ((tetR,+1))\n
((lacI,2),(tetR,3));((cI,1)) -3-> ((cI,+1))\n
 
#### Mandatory activities
 
They are defined in the same way as the potential ones but must be separated with once again "%%"
 \nexample:\n
 
();() -1-> ((tetR,+2))\n
((tetR,1));() -2-> ((tetR,-2))\n

#### Initial marking

The inital marking will define at what level each entity will begin.
It is seprated from the mandatory activities by "%%", and definied in one block
 \nexample:\n
 
(tetR,1)
(cI,0)
(lacI,3) 