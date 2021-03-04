BOUNCE:
~~~~~~

'Bounce' is a game played by a single player. The aim of the player is that is he makes the ball pass through an opening at the top to win the game. 
The player has dodge the walls and avoid spikes before reaching the top. The player loses a life and has to start from the beginning if the ball touches a spike. So Beware!
The game is played using the 'cursor keys' and to jump, make use of 'spacebar'.

1. map.txt:

This is where the plan of the game is. It shows the Player(ball), walls, spikes and other obstacles in the form of 'characters'. 
The code is written based on this.

2. settings.txt:

This is where all the things required are declared. The colours used in the game are mentioned with their RGB values.
The lenght and width of screen is declared here. the other stuff like 'frames per second', backgrund colour, tile size,grid length and grid width are declared here.

3. tilemap.txt:

This file is basically to control camera so as that it goes ppropriately with the ball. The camera is such that the ball always stays in middle except for the places where it reaches the end of the screen.

4. sprites.py:

This is for taking care of size, colour and background of the ball.
The appropriate movements, collision of ball with the walls, making the ball jump higher and making the ball bounce are all declared in this function

5. Main.py:

This is where all the programs are called and collaborated. Here, 
(a)the clock is set, 
(b)code is written so as to display the caption,
(c)load the game
(d)the operations required to play the game are declared
(e)the background sounds are also set here
(f)the appearence of start screen, game screen, game over screen are set here

