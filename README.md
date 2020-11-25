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
python3 AI_connect6.py

# Play against a Random Player
python3 AI_connect6.py -rand

# AI vs AI
python3 AI_connect6.py -ai
```

## Demo Video

[![Watch the video](demo.png)](https://drive.google.com/file/d/1XFZcxCoZbel-q1nowbzPBr3_L3W06thB/view?usp=sharing)

## Sources

**code to help create board game grid**: https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame 

**starter code for victory screens**: https://pythonprogramming.net/displaying-text-pygame-screen/

**code to get diagonals in a 2-D list**: https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python
