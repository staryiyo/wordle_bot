import asyncio
import logging
from datetime import date
from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder

from wordle import load_words, get_daily_word, check_guess, render_board, WORDS
from database import init_db, get_today_game, save_game, get_stats

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class GameState(StatesGroup):
    choosing = State()
    playing = State()

def mode_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🇷🇺 Русский 5 букв", callback_data="mode_ru5")
    builder.button(text="🇷🇺 Русский 6 букв", callback_data="mode_ru6")
    builder.button(text="🇬🇧 English 5 letters", callback_data="mode_en")
    builder.adjust(1)
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я Wordle-бот 🟩\n\n"
        "Угадай слово за 6 попыток.\n"
        "🟩 — буква на своём месте\n"
        "🟨 — буква есть, но не там\n"
        "⬜ — буквы нет в слове\n\n"
        "Напиши /play чтобы начать!"
    )

@dp.message(Command("play"))
async def cmd_play(message: Message, state: FSMContext):
    await state.set_state(GameState.choosing)
    await message.answer("Выбери режим игры:", reply_markup=mode_keyboard())

@dp.callback_query(lambda c: c.data.startswith("mode_"))
async def mode_chosen(call: CallbackQuery, state: FSMContext):
    mode = call.data.replace("mode_", "")
    user_id = call.from_user.id
    today = str(date.today())
    game_key = f"{today}_{mode}"

    if get_today_game(user_id, game_key):
        await call.message.edit_text("Ты уже играл в этом режиме сегодня. Возвращайся завтра! 🕐\nСтатистика: /stats")
        return

    words = load_words(WORDS[mode])
    word = get_daily_word(words)

    await state.set_state(GameState.playing)
    await state.update_data(word=word, mode=mode, attempts=[], guesses=[])
    await call.message.edit_text(
        f"Режим: {'🇷🇺 Русский 5 букв' if mode == 'ru5' else '🇷🇺 Русский 6 букв' if mode == 'ru6' else '🇬🇧 English 5 letters'}\n\n"
        f"Игра началась! Введи первое слово из {'6' if mode == 'ru6' else '5'} букв 👇"
    )

@dp.message(GameState.playing)
async def handle_guess(message: Message, state: FSMContext):
    data = await state.get_data()
    word = data["word"]
    mode = data["mode"]
    attempts = data["attempts"]
    guesses = data["guesses"]
    word_len = len(word)

    guess = message.text.strip().lower()

    if len(guess) != word_len:
        await message.answer(f"Введи слово ровно из {word_len} букв!")
        return

    if mode in ("ru5", "ru6"):
        if not all(c in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" for c in guess):
            await message.answer("Только русские буквы!")
            return
    else:
        if not guess.isalpha() or not all(c in "abcdefghijklmnopqrstuvwxyz" for c in guess):
            await message.answer("English letters only!")
            return

    result = check_guess(word, guess)
    attempts.append(result)
    guesses.append(guess)
    board = render_board(attempts, guesses)
    attempts_left = 6 - len(attempts)

    if all(r == "correct" for r in result):
        await state.clear()
        save_game(
            user_id=message.from_user.id,
            username=message.from_user.username or "",
            date=f"{str(date.today())}_{mode}",
            word=word,
            solved=True,
            attempts_count=len(attempts)
        )
        await message.answer(
            f"{board}\n\n"
            f"🎉 Верно! Слово: *{word.upper()}*\n"
            f"Угадал за {len(attempts)} попыток!",
            parse_mode="Markdown"
        )
        return

    if len(attempts) >= 6:
        await state.clear()
        save_game(
            user_id=message.from_user.id,
            username=message.from_user.username or "",
            date=f"{str(date.today())}_{mode}",
            word=word,
            solved=False,
            attempts_count=6
        )
        await message.answer(
            f"{board}\n\n"
            f"😔 Не угадал. Слово было: *{word.upper()}*",
            parse_mode="Markdown"
        )
        return

    await state.update_data(attempts=attempts, guesses=guesses)
    await message.answer(f"{board}\n\nОсталось попыток: {attempts_left}")

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