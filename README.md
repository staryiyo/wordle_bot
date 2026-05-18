# Wordle Telegram Bot 🟩🟨⬜

## Project Description
A fully functional Telegram bot that brings the popular game Wordle to your chats. Users try to guess a secret daily word within 6 attempts, receiving color-coded emoji feedback for each guess. Built as a Final Project for the Software Engineering program, this bot handles multiple concurrent users and tracks individual player statistics.

## Features
* **Multiple Game Modes:** Play in Russian (5-letter or 6-letter words) or English (5-letter words).
* **Interactive UI:** Utilizes Telegram's Inline Keyboards for seamless navigation and mode selection.
* **State Management:** Uses a Finite State Machine (FSM) to isolate and handle concurrent user sessions without overlap.
* **Data Persistence:** Player statistics and game history are saved to an SQLite database and automatically backed up to an external `backup_stats.json` file.
* **OOP Architecture:** Core game mechanics are cleanly encapsulated within custom Python classes.

## Technologies Used
* **Language:** Python 3.10
* **Bot Framework:** `aiogram` (v3.4.1)
* **Database:** `sqlite3` (built-in)
* **Environment Management:** `python-dotenv`
* **Testing:** `unittest` (built-in)

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd wordle_bot


   Create and activate a virtual environment:
    Bash

    python -m venv venv

    # For Windows:
    venv\Scripts\activate

    # For macOS/Linux:
    source venv/bin/activate

    Install the required dependencies:
    Bash

    pip install -r requirements.txt

    Create a .env file in the root directory and add your Telegram Bot Token (obtained from @BotFather):
    Фрагмент кода

    BOT_TOKEN=your_token_here

How to Run the Project

To start the bot, run the main script from your terminal:
Bash

python bot.py

To run the unit tests and verify the core game logic:
Bash

python test_wordle.py

# Screenshots

   <img width="793" height="326" alt="изображение" src="https://github.com/user-attachments/assets/b1c9fd87-b0eb-4290-a8da-3e00c8cdf560" />
    <img width="776" height="268" alt="изображение" src="https://github.com/user-attachments/assets/e13f2727-8682-4abf-85f2-52fafb2f128f" />
    <img width="768" height="250" alt="изображение" src="https://github.com/user-attachments/assets/12d7da6d-d3d8-44df-a728-c590088fb570" />
    <img width="749" height="311" alt="изображение" src="https://github.com/user-attachments/assets/943b0bd3-c679-4bb8-bde6-f56b615e88e4" />
    <img width="770" height="214" alt="изображение" src="https://github.com/user-attachments/assets/60e137cd-f2e7-4684-97db-c8e23bc27b7b" />



# Team Members & Roles
 
      Group: SE-2513
      
    Alizhan Rymkhan : Core Game Logic & OOP. Developed the WordleGame class, custom performance decorators, and the word-validation algorithms.

    Shangerey Adilbek : Telegram API Integration. Implemented aiogram handlers, the Finite State Machine (FSM), and interactive inline keyboards.

    Yerketay Zhanserik : Data Persistence & QA. Designed the SQLite database schema, implemented the JSON backup functionality, and wrote unit tests for code robustness.
