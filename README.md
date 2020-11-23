# Connect6
Assignment 4 Project

This Connect6 program has two modes: 

- Player vs Player
- Player vs AI (negamax)
- AI vs Random Player
- AI vs AI

## To Run

**NOTE**: Tested on Python 3.6, might not work as intended on the latest Python releases

```bash
# Install pygame
python3 -m pip install pygame

# Install pygame_menu
python3 -m pip install pygame_menu

# To run
python3 pvp_connect6.py
```

## Accessing AI's Different Modes Without Using the Menu

```bash
# Play against an AI
python3.6 AI_connect6.py

# Play against a Random Player
python3.6 AI_connect6.py -rand

# AI vs AI
python3.6 AI_connect6.py -ai
```
