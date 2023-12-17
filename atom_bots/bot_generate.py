import asyncio
import logging
import torch
from aiogram.filters import Command
from transformers import pipeline
from aiogram import Bot, Dispatcher, types

bot = Bot(token="6834162026:AAE4tPhJbqt5coUs1l_Y0Ooqs15mx-S83FY")
dp = Dispatcher()

model = "Denis431/docs_generate_v2"


try:
    # Try to use CUDA
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pipe = pipeline("text-generation", model=model, device=device, max_length=250)
except Exception as e:
    # If there's an exception (e.g., CUDA not available), fall back to CPU
    print(f"An error occurred: {e}")
    print("Falling back to CPU.")
    device = torch.device("tpu")
    pipe = pipeline("text-generation", model=model, device=device, max_length=250)


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        text="Привет! Бот позволяет вам получать ответы на вопросы связанные с темой закопкок в атомной отрасли, "
             "в том числе с нормативно-правовыми актами.\n⚡ Бот использует собственную модель, которая была обучена с нуля "
             "на GPT.\n✉ Чтобы получить текстовый ответ, напишите свой вопрос в чат.\nУдачного пользования!")


@dp.message()
async def echo_message(message: types.Message):
    answer = pipe(message.text, num_return_sequences=1)[0]["generated_text"]
    await message.answer(text=answer)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
