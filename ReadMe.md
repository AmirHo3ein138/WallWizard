# Quoridor-like Console Game – Group Project (IUST)

This project was developed as a **group project** in collaboration with my classmates at **Iran University of Science and Technology (IUST)** as part of our **Bachelor curriculum**.  
It is a **console-based, two-player board game inspired by Quoridor**, featuring user account management, persistent statistics, save/load functionality, and a colorful terminal UI.

---

## Key Features
- 🎮 **Two-Player Gameplay**: Turn-based logic with piece movement, wall placement (vertical & horizontal), and path validation.  
- 🔒 **User Authentication**: Registration & login with secure password hashing (**bcrypt**).  
- 💾 **Save & Load**: Save game progress as JSON and resume later from the main menu.  
- 🏆 **Leaderboard**: Tracks wins and losses for all registered players, sorted dynamically.  
- 🎨 **Terminal UI**: Colored board and formatted tables using **rich** and **colorama**.  
- 🛡️ **Rule Enforcement**: Validates moves and ensures no player can be completely blocked (via DFS-based path checking).  

---

## Technologies & Libraries
- **Python 3.x**  
- **rich** – Fancy terminal output (tables, colors, formatting)  
- **colorama** – ANSI color support in terminal  
- **bcrypt** – Password hashing for secure login  
- **msvcrt** – For hidden password input (Windows-only)  
- **json**, **os**, **uuid**, **time**, **re**, **sys** – Standard library utilities  

---

## How It Works
1. **Player Accounts:** Each player signs up or logs in; profiles are stored in JSON format under the `players/` directory.  
2. **Gameplay:** Two players take turns moving their pieces or placing walls to block the opponent’s path.  
3. **Wall Placement Rules:** The game prevents illegal wall placements using DFS to ensure both players still have a valid path to their target.  
4. **Saving Progress:** Players can save the current game state (stored as JSON in the `saved_games/` directory).  
5. **Leaderboard:** All player stats (wins/losses) are tracked and displayed in a ranking table.  
