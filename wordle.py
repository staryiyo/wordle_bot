from datetime import date
import os
import functools
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Словарь путей к файлам слов
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

# Декоратор для выполнения требований силлабуса
def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        print(f"[LOG] Функция {func.__name__} выполнена за {duration:.6f} сек.")
        return result
    return wrapper

# Функция загрузки слов, которую искал бот
def load_words(path: str) -> list[str]:
    with open(path, encoding="utf-8") as f:
        words = [line.strip().lower() for line in f if line.strip()]
    return list(set(words))

# Функция выбора ежедневного слова
def get_daily_word(words: list[str]) -> str:
    day_number = (date.today() - date(2024, 1, 1)).days
    return words[day_number % len(words)]

# Функция отрисовки игрового поля
def render_board(attempts: list[list[str]], guesses: list[str]) -> str:
    lines = []
    for i in range(len(attempts)):
        emoji_row = "".join(EMOJI[status] for status in attempts[i])
        lines.append(f"{emoji_row}  `{guesses[i].upper()}`")
    return "\n".join(lines)


class WordleGame:
    """Класс, инкапсулирующий состояние одной игровой сессии (Требование ООП)"""
    def __init__(self, secret_word: str, mode: str):
        self.secret_word = secret_word.lower()
        self.mode = mode
        self.word_len = len(secret_word)
        self.max_attempts = 6

    @log_action 
    def check_user_guess(self, guess: str) -> list[str]:
        """Логика проверки введенного слова"""
        guess = guess.lower()
        result = ["absent"] * self.word_len
        answer_chars = list(self.secret_word)

        # Первый проход: точные совпадения
        for i in range(self.word_len):
            if guess[i] == self.secret_word[i]:
                result[i] = "correct"
                answer_chars[i] = None

        # Второй проход: буквы не на своих местах
        for i in range(self.word_len):
            if result[i] == "correct":
                continue
            if guess[i] in answer_chars:
                result[i] = "present"
                answer_chars[answer_chars.index(guess[i])] = None

        return result