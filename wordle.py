from datetime import date

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WORDS = {
    "ru5": os.path.join(BASE_DIR, "words.txt"),
    "ru6": os.path.join(BASE_DIR, "words_ru6.txt"),
    "en": os.path.join(BASE_DIR, "words_en.txt"),
}

EMOJI = {
    "correct": "🟩",
    "present": "🟨",
    "absent": "⬜"
}

def load_words(path: str) -> list[str]:
    with open(path, encoding="utf-8") as f:
        words = [line.strip().lower() for line in f if line.strip()]
    return list(set(words))

def get_daily_word(words: list[str]) -> str:
    day_number = (date.today() - date(2024, 1, 1)).days
    return words[day_number % len(words)]

def check_guess(answer: str, guess: str) -> list[str]:
    result = ["absent"] * len(answer)
    answer_chars = list(answer)

    for i in range(len(answer)):
        if guess[i] == answer[i]:
            result[i] = "correct"
            answer_chars[i] = None

    for i in range(len(answer)):
        if result[i] == "correct":
            continue
        if guess[i] in answer_chars:
            result[i] = "present"
            answer_chars[answer_chars.index(guess[i])] = None

    return result

def render_board(attempts: list[list[str]], guesses: list[str]) -> str:
    lines = []
    for i, result in enumerate(attempts):
        emojis = " ".join(EMOJI[r] for r in result)
        letters = " ".join(guesses[i].upper())
        lines.append(f"{emojis}  {letters}")
    return "\n".join(lines)