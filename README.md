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
