## ShootyBangSpaceWars

As a freelance space pilot you know of all the threats that can be lurking behind every asteroid and planet, however you never could have expected what was ahead of you as the galaxy seems to implode and brings some of the most ferocious pilots together for one final face off. Your survival will be dependent completely on your skills as a pilot. Good luck.

# Summary

Ideas:
- Spaceship deathmatch
- Orbital mechanics
- Can only thrust and fire in the spinal direction of ship
- Can rotate.
- Firing bullets ejects mass etc.
- Choose to allocate energy to shield, weapon or thrusters
- Energy recovers quicker around light due to solar panels.
- Energy depletes through use
- space anomolies e.g. blackholes, light bursts.
- varying game modes.
- damage will effect how much energy you can put in each department. (random)

# Tasks
- Get a basic window up and running. DONE
- Spacestation bases.
- Gravity.
- Energy distribution.
- Weapons.
- Awesome music.
- Multiplayer.
- Sprites.
- View Panning TJD

# Controls
- up arrow - move forward
- left arrow - runs thruster on the left
- right arrow - runs thruster on the right

- Q - increase energy on weapons
- W - increase energy on shields
- E - increase energy on thrusters
- A - decrease energy on weapons
- S - decrease energy on shields
- D - decrease energy on thrusters

- Spacebar - Shoot
- Tab - Open up scoreboard
- Esc - Open menu

menu controls
- up - move up selection
- down - move down selection
- enter - select

# Energy
- 5 points of energy
- level 1 - 5 - energy goes from level 1 to 5 for each level

- weapons
  - level 1 - single shot
  - level 2 - multi shot
  - level 3 - triple shot
  - level 4 - quad shot
  - level 5 - burst shot
- shields
  - level 1 - small front facing shield
  - level 2 - large front facing shield
  - level 3 - small side and front facing shield
  - level 4 - small back, side and front facing shield
  - level 5 - full shield
- Thrusters
  - level 1 - slow
  - level 2 - slow / medium
  - level 3 - medium
  - level 4 - medium / fast
  - level 5 - fast
  
  # Sound files
  Advised that it'll be finished by 2pm. 
  - thrusters
  - lasers
  - shield
  - explosion
  - crash
  - background music



  #Dev

  ## Packet format

- Map
	- Planets[]
		- pos
			- x (double)
			- y (double)
		- mass (double)
		- radius (double)
		- type (e.g. SUN, MARS, EARTH) (string)

- State
	- Ships[]
		- pos
			- x (double)
			- y (double)
			- angle (double)
		- id (string)
		- energy (double)
		- damage (double)
	- Bullets[]
		-pos
			- x (double)
			- y (double)
			- angle (double)

- Controls
	- right (bool)
	- left (bool)
	- forward (bool)
	- shoot (bool)

