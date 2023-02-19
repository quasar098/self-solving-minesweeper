# self solving minesweeper

**todo: make this start when there is no input detected for some time**

it solves itself

this is inspired by [have a luke at this](https://github.com/haveaLukeatthis/SelfSolvingMinesweeper)

## install requirements

use `pip install -r /path/to/requirements.txt`

note: if something doesn't work, use python 3.9+ if you aren't already

## config.json

this  is the configuration file to edit the settings

- `bomb_percent` is the percentage of bombs 
- `rng_carry` means that the algorithm will "cheat" a little and always survive 50/50s
- `playable` means that you can play the minesweeper instead of having it solve itself. press `<ESC>` to exit the application when in playable mode
- `anim_speed` is how fast the cascades are. lower speed = laggier feel, so beware!