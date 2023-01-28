# Maze (with pacman styling)

## Requirements for launch
You need Python 3.7+ version, time module (python built-in) and [pygame](https://pypi.org/project/pygame/) to launch the game.

If you don't have pygame package, use the pip (in terminal) to install it:
```bash
pip install pygame
```

## Launching
Execute the **maze.py** file.

## Controls & Gameplay
- Use arrow keys or WASD to move.
- Press the space button to shoot.
- To win the game, you need to get to the star object in the bottom left corner of the screen.
- You also can collect bonus strawberry object.

## Game modification
- If you need to modify screen size, modify WIDTH and HEIGHT constants in 7 and 9 lines.

- If you need to modify character's or bullet's speed, modify player_speed and bullet_speed in 150 and 151 lines.

- If you need to modify enemies' speed, modify self.speed in 91 line.

***These changes can and will cause some bugs and errors and are not recommended.***
