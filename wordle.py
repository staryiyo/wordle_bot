from datetime import date

EMOJI = {
    "correct": "🟩",
    "present": "🟨",
    "absent": "⬜"
}

def load_words(path: str = "words.txt") -> list[str]:
    with open(path, encoding="utf-8") as f:
        words = [line.strip().lower() for line in f if len(line.strip()) == 5]
    return list(set(words))

def get_daily_word(words: list[str]) -> str:
    day_number = (date.today() - date(2024, 1, 1)).days
    return words[day_number % len(words)]

def check_guess(answer: str, guess: str) -> list[str]:
    result = ["absent"] * 5
    answer_chars = list(answer)

    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = "correct"
            answer_chars[i] = None

    for i in range(5):
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