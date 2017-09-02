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

(optional)
- 1-9 - Special equipment usage
- r - increase energy on HUD
- f - decrease energy on HUD

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
- HUD??
  - level 1 - shows energy usage, shows equipment and shows radar
  - level 2 - shows hull damage, shows equipment energy usage, (what points are being used where)
  - level 3 - unlock showing allies on radar and planets
  - level 4 - radar shows enemies and asteroids
  - level 5 - shows gravitational pull and special equipment on screen
  
  # Sound files
  Advised that it'll be finished by 2pm. 
  - thrusters
  - lasers
  - shield
  - explosion
  - crash
  - background music

# HUD

- Scoreboard
- Radar
  - enemies (red dots)
  - team mates (green dots)
  - asteroids & planets
- Hull
- Energy
- Equipment
  - icons of thrusters, shield, weapons, HUD.
  - 5 points underneath to show how many energy points are in each equipment
- Special Equipment?? - collect metal from killing enemies and mining, take it back to your spacestation and build it. If you die you drop all metal.
  - Cloak - Hides from radar
  - Mines - Drop and leave on map
  - Rockets - Avoids Shields
  - Nitro - Gives an extra boost on thrusters in a forward direction
  - repair bots - repairs damage over time.
- gravitational pull


# Dev

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
		- pos
			- x (double)
			- y (double)
			- angle (double)

- Controls
	- right (bool)
	- left (bool)
	- forward (bool)
	- shoot (bool)