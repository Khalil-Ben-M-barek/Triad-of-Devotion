# Triad of Devotion

A turn-based strategy game featuring a **Potential Breach** system that charges when taking damage, **Synergy Abilities** that require coordination and strategy, real-time **blocking**, boss capable of **seizing control** of heroes to turn them against each other, customizable **spell** loadouts before battle, and a **turn limit** designed to force near-perfect strategic plays.

## How to Play (Python Not Required)

The game is compiled into a standalone executable, so you do not need Python or Pygame installed to play.

1. Go to the **Releases** section on the right side of this GitHub page.
2. Download the latest version of Triad of Devotion.
3. Extract the ZIP file and double-click the executable to launch the game.

## Controls
* **Arrow Keys**: Menu navigation
* **Tab Key**: Toggle menus in equip menu
* **Spacebar**: Confirm selection
* **L Key**: Elena's block key
* **O Key**: Ethan's block key
* **V Key**: Evelyn's block key

## For Developers / Running from Source

If you want to modify the code or run it natively, follow the setup steps below for your operating system.

### 1. Clone the Repository

Open your terminal or command prompt (keep it open for the next step) and run:

```bash
git clone https://github.com/Khalil-Ben-M-barek/Triad-of-Devotion.git
cd "Triad of Devotion"
```

---
### 2. Install Dependencies and Run
#### Windows

1. Download and install the latest version of Python from [python.org](https://www.python.org/downloads/).

2. Make sure to check the **Add python.exe to PATH** box at the bottom of the installer window before clicking install

3. Run the following commands:

```bash
python -m venv venv
venv\Scripts\activate
pip install pygame
python main.py
```

---

#### macOS

Run the following commands:

```bash
nix-shell -p python3
python3 -m venv venv
source venv/bin/activate
pip install pygame
python3 main.py
```

---

#### Linux

Run the following commands:

```bash
nix-shell -p python3
python3 -m venv venv
source venv/bin/activate
pip install pygame
python3 main.py
```

