import asyncio
import logging
from datetime import date
from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from wordle import load_words, get_daily_word, check_guess, render_board
from database import init_db, get_today_game, save_game, get_stats

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

WORDS = load_words()

class GameState(StatesGroup):
    playing = State()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я Wordle-бот 🟩\n\n"
        "Угадай слово из 5 букв за 6 попыток.\n"
        "🟩 — буква на своём месте\n"
        "🟨 — буква есть, но не там\n"
        "⬜ — буквы нет в слове\n\n"
        "Напиши /play чтобы начать!"
    )

@dp.message(Command("play"))
async def cmd_play(message: Message, state: FSMContext):
    user_id = message.from_user.id
    today = str(date.today())

    if get_today_game(user_id, today):
        await message.answer("Ты уже играл сегодня. Возвращайся завтра! 🕐\nСтатистика: /stats")
        return

    word = get_daily_word(WORDS)
    await state.set_state(GameState.playing)
    await state.update_data(
        word=word,
        attempts=[],
        guesses=[],
        message_id=None
    )
    await message.answer("Игра началась! Введи первое слово из 5 букв 👇")

@dp.message(GameState.playing)
async def handle_guess(message: Message, state: FSMContext):
    data = await state.get_data()
    word = data["word"]
    attempts = data["attempts"]
    guesses = data["guesses"]

    guess = message.text.strip().lower()

    if len(guess) != 5 or not guess.isalpha():
        await message.answer("Введи слово ровно из 5 букв!")
        return

    if not all(c in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" for c in guess):
        await message.answer("Только русские буквы!")
        return

    result = check_guess(word, guess)
    attempts.append(result)
    guesses.append(guess)

    board = render_board(attempts, guesses)
    attempts_left = 6 - len(attempts)

    if all(r == "correct" for r in result):
        await state.clear()
        save_game(user_id=message.from_user.id,
                  username=message.from_user.username or "",
                  date=str(date.today()),
                  word=word,
                  solved=True,
                  attempts_count=len(attempts))
        await message.answer(
            f"{board}\n\n"
            f"🎉 Верно! Слово: *{word.upper()}*\n"
            f"Угадал за {len(attempts)} попыток!",
            parse_mode="Markdown"
        )
        return

    if len(attempts) >= 6:
        await state.clear()
        save_game(user_id=message.from_user.id,
                  username=message.from_user.username or "",
                  date=str(date.today()),
                  word=word,
                  solved=False,
                  attempts_count=6)
        await message.answer(
            f"{board}\n\n"
            f"😔 Не угадал. Слово было: *{word.upper()}*",
            parse_mode="Markdown"
        )
        return

    await state.update_data(attempts=attempts, guesses=guesses)
    await message.answer(
        f"{board}\n\n"
        f"Осталось попыток: {attempts_left}"
    )

@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    row = get_stats(message.from_user.id)
    if not row:
        await message.answer("Ты ещё не играл! Напиши /play")
        return
    total, wins = row
    winrate = round(wins / total * 100) if total > 0 else 0
    await message.answer(
        f"📊 Твоя статистика:\n\n"
        f"Игр сыграно: {total}\n"
        f"Побед: {wins}\n"
        f"Винрейт: {winrate}%"
    )

async def main():
    init_db()
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())