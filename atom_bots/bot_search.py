import asyncio
import logging
import json
import torch
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModel

bot = Bot(token="")
dp = Dispatcher()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
embeddings_dataset = load_dataset("Denis431/atomic_data")
automarkup_dataset = load_dataset('csv', data_files={
    "test": 'datasets/answer_ds.csv',
})

# Load model and tokenizer from HuggingFace Hub
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/multi-qa-mpnet-base-dot-v1")
model = AutoModel.from_pretrained("sentence-transformers/multi-qa-mpnet-base-dot-v1")


# CLS Pooling - Take output from first token
def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0]


# Encode text
def encode(texts):
    # Tokenize sentences
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input, return_dict=True)

    # Perform pooling
    embeddings = cls_pooling(model_output)

    return embeddings


def search(query):
    # Sentences we want sentence embeddings for
    docs = embeddings_dataset["train"]["answer"]
    doc_emb = embeddings_dataset["train"]["embeddings"]

    # Encode query and docs
    query_emb = encode(query)

    doc_emb_tensor = torch.tensor(doc_emb)  # Convert doc_emb to a tensor
    scores = torch.mm(query_emb, doc_emb_tensor.transpose(0, 1))[0].cpu().tolist()

    doc_score_pairs = list(zip(embeddings_dataset["train"]["query"], docs, scores))

    # Sort by decreasing score
    doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[2], reverse=True)
    text = "Релевантые ответы"
    count = 1
    for query, answer, score in doc_score_pairs[:3]:
        text += f"\n{count}) Ответ: {answer}. Score {score}"
        count += 1
    text+="\nВыберите самый релевантный ответ по вашему мнению, для улучшения работы модели)"
    return text


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        text="Привет! Бот позволяет вам получать ответы на вопросы связанные с темой закопкок в атомной отрасли, "
             "в том числе с нормативно-правовыми актами.\n⚡ Бот использует собственную модель, которая была дообучена "
             "на sBERT модели.\n✉ Чтобы получить текстовый ответ, напишите свой вопрос в чат.\nУдачного пользования!")


@dp.message()
async def echo_message(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="1",
        callback_data="1")
    )
    builder.add(types.InlineKeyboardButton(
        text="2",
        callback_data="2")
    )
    builder.add(types.InlineKeyboardButton(
        text="3",
        callback_data="3")
    )
    answer = search(message.text)
    await message.answer(text=answer, reply_markup=builder.as_markup())


@dp.callback_query(F.data == "1")
async def send_random_value(callback: types.CallbackQuery):
    message = callback.message.text.split("\n")
    print("Запись ответа в JSON")
    await callback.message.answer("Спасибо за ответ!")


@dp.callback_query(F.data == "2")
async def send_random_value(callback: types.CallbackQuery):
    message = callback.message.text.split("\n")
    print("Запись ответа в JSON")
    await callback.message.answer("Спасибо за ответ!")


@dp.callback_query(F.data == "3")
async def send_random_value(callback: types.CallbackQuery):
    print("Запись ответа в JSON")
    await callback.message.answer("Спасибо за ответ!")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
