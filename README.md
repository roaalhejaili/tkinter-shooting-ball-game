
# Shooting Balls Game (HCI 418 Project)

The **Shooting Balls Game** is a 2D interactive desktop game developed using **Python** and the **Tkinter** GUI library.  
This project was created as part of the **HCI 418 course** and demonstrates principles of **human–computer interaction**, **basic physics simulation**, and **event-driven programming**.

The objective of the game is to destroy all moving balls on the screen using a controllable cannon before the timer runs out.

---

## System Requirements
- Operating System: Windows, macOS, or Linux
- Python version: Python 3.8 or higher
- Required libraries (included with Python):
  - tkinter
  - math
  - random

No external or third-party libraries are required.

---

## Installation
1. Install Python 3.8 or later.
2. On Windows, make sure **“Add Python to PATH”** is selected.
3. Verify installation:
```bash
python --version
````

---

## Running Instructions

1. Download or clone the project repository.
2. Ensure the following files are in the same directory:

   * `Team118_code.py`
   * `README.md`
3. Open a terminal or command prompt.
4. Navigate to the project directory:

```bash
cd path/to/shooting-balls-game-hci418
```

5. Run the game:

```bash
python Team118_code.py
```

6. The game window will open automatically.

---

## User Interface Overview

The game interface consists of:

* A main play area where balls move and bullets are fired
* A control panel containing buttons and sliders
* A status bar displaying real-time game information (score, level, targets, time, status)

---

## Controls

### Buttons

* **Start Game** – Starts or resumes the game
* **Pause / Resume** – Pauses or continues gameplay
* **Stop All** – Stops the game and resets progress
* **Restart Game** – Restarts the game from Level 1
* **SHOOT!** – Fires a bullet

### Sliders (Cannon Settings)

* **Angle (0–90°)** – Controls shooting angle
* **Barrel Length** – Adjusts visual barrel length and bullet start position
* **Power / Strength** – Controls bullet speed and barrel thickness
* **Vertical Position** – Moves the cannon up or down

### Keyboard Controls

* **Space** – Shoot
* **P** – Pause / Resume
* **Up Arrow** – Increase cannon angle
* **Down Arrow** – Decrease cannon angle
* **Left Arrow** – Move cannon downward
* **Right Arrow** – Move cannon upward

---

## Gameplay

* Adjust sliders to control angle, power, and position
* Fire bullets using the SHOOT button or Space key
* Destroy all balls before the timer reaches zero
* Complete a level to advance to the next one

---

## Scoring System

* Each ball awards points based on its size
* Larger balls give higher scores
* Score accumulates across all levels
* Final score is shown when the game ends

---

## Level System

* Maximum of **3 levels**
* Difficulty increases by:

  * Increasing the number of balls
  * Increasing ball speed
  * Reducing available time (minimum 15 seconds)
* A notification appears when a level is completed

---

## Physics Implementation

* Bullets move using linear velocity equations
* Balls bounce off walls
* Ball-to-ball collisions are elastic (conservation of momentum)
* Ball mass is calculated from radius and density

---

## Technical Details

* Game update interval: 20 ms
* Timer update interval: 1 second
* Animation handled using Tkinter `after()` method
* Object-Oriented Programming (OOP) structure

---

## Known Limitations

* No sound effects or background music
* No save/load functionality
* Limited number of levels
* Simplified physics model

---

## Future Improvements

* Add sound effects and music
* Add difficulty selection
* Add more levels or endless mode
* Improve graphics and animations
* Save high scores

---

## Group Contribution

This was a **group project**, and all members contributed collaboratively.


---

## Developers

**Team118 – Roaa, Walaa, Juri, Bushra**
Course: HCI 418

---

## License

This project was developed for educational purposes and may be freely used or modified.

````

---

````
