## Extincion JR: a boardgame simulation


### The origin of the simulation

This is a simulation of a **boardgame prototype** (provissionally) named Extinción Junior, for it is a simplified and cooperative version of the card game **¡Extinción!, by David GJ**, an Spanish designer, also known by being the illustrator of the worldwide **famous card game Virus!** (by S. Santisteban, D. Cabrero and C. López). 

This Extinción Junior is a game designed for 3-6 years old children and it is cooperative. This simulation is now implemented as its basic mode, which is orientated to 4-5 years old children. 

### The objective of the simulation
My goal was to advise the author on the game design so he could adjust the number of tokens. In the simulation, we specifically study the number of __"comodinos"__ which are wildcard or joker tokens and how this number changes drastically the probability of winning the game. 

### The code

First of all, the code has a lot of prints so I could understand correctly and debug properly while I was working on it. That is why I wrote "DEBUG = False" so I can change it to True whether I want to develop some part of the code again.

Apart from that, we have the setup of the game in three functions:
- generar_mazo(): which is generating the cards (there are only 10 cards but every one of them are different). They are 10 different dinosaurs who eat a different amount of food (leaves, meat, fish and bones).
- generar_bolsa(): which generates the bag with the food tokens and "comodinos" tokens. One joker token can be eaten by any of the dinosaurs so the more joker tokens we have, the easier we win the game. Remember this is a cooperative game and we have to feed the dinosaurs before the extinction comes. 
- preparar_partida(): this establish the status of the game "estado" (the deck "mazo", the discards "descartes", the center of the table "mesa" with the dinosaurs to feed, the extinction board "extincion" -a countdown where we put the tokens if they don't match any of the dinosaurs in the table-, the bag "bolsa" with the tokens and the turn "turno" starting from 0).

Then we have the win and lose functions and 3 specific functions for the development of the game:
- rescatar_dino(): it applies when a dinosaur card in the center of the table is fully fed. It is rescued!
- alimentar_dino_hambriento(): this is the basic code which applies for "comodinos", so it can be fed and substitute any food.
- colocar_ficha(): we can only put a token on a dinosaur to feed it if it needs one of the tokens we do have in our hands.

Finally we have the partida() function so we can organize the game step by step.
Iniciar_partida() will set everything up for us to return the results we want to simulate (number of comodinos used, number of rescued dinosaurs at the end of the game, whether the game was won or lost and the number of turns).


### Usage

This simple code is just using random and pandas (so we can generate dataframes and save them to analyze them).


### Next steps

Of course I want to improve the code in several ways:
- I want to code a yet simpler version of this game so I can check if it is playable by even younger children (maybe 3-4 years old). I need to simulate then how it changes depending on the number of comodinos and the number of spaces in the extinction countdown.
- I want to code a little more "intelligent" (not so random) AI so it does not play like a 4-yo child but maybe 5 or even 6 yo. 
- I want to code an advanced version of the game which introduces a new kind of token which may be much more difficult depending from the person and could be a challenge to program a "6-7 year old Artificial Intelligence" who win this version of game.
