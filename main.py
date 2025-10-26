import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from aiogram.enums import ParseMode
import asyncio
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8451963488:AAFNwy9zq0savVxNX6-9sm5dSto7pcTTxKY"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

IMAGE_PATHS = {
    "main": "images/2.jpg"
}

def get_main_menu_keyboard():
    keyboard = [
        [
            types.InlineKeyboardButton(text="Инфо", callback_data="info"),
            types.InlineKeyboardButton(text="Сотрудничество", callback_data="cooperation")
        ],
        [
            types.InlineKeyboardButton(text="Канал с темками", callback_data="themes")
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)

async def send_or_edit_photo(callback: types.CallbackQuery, image_key: str, caption: str, reply_markup=None):
    try:
        if os.path.exists(IMAGE_PATHS[image_key]):
            with open(IMAGE_PATHS[image_key], 'rb') as file:
                photo_data = file.read()
            
            if callback.message.photo:
                await callback.message.edit_media(
                    media=types.InputMediaPhoto(
                        media=BufferedInputFile(photo_data, filename=f"{image_key}.jpg"),
                        caption=caption
                    ),
                    reply_markup=reply_markup
                )
            else:
                await callback.message.answer_photo(
                    photo=BufferedInputFile(photo_data, filename=f"{image_key}.jpg"),
                    caption=caption,
                    reply_markup=reply_markup
                )
        else:
            await callback.message.edit_caption(
                caption=caption,
                reply_markup=reply_markup
            )
            
    except Exception as e:
        logger.error(f"Ошибка загрузки картинки {image_key}: {e}")
        await callback.message.edit_caption(
            caption=caption,
            reply_markup=reply_markup
        )

@dp.message(Command("start"))
async def cmd_start(message: Message):
    try:
        if os.path.exists(IMAGE_PATHS["main"]):
            with open(IMAGE_PATHS["main"], 'rb') as file:
                photo_data = file.read()
            
            await message.answer_photo(
                photo=BufferedInputFile(photo_data, filename="main.jpg"),
                caption="Добро пожаловать! Выберите раздел:",
                reply_markup=get_main_menu_keyboard()
            )
        else:
            await message.answer(
                "Добро пожаловать! Выберите раздел:",
                reply_markup=get_main_menu_keyboard()
            )
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.answer("Ошибка загрузки")

@dp.callback_query(lambda c: c.data == "info")
async def show_info(callback: types.CallbackQuery):
    caption = (
        "🔗 SILVERSTEAMS – это проект, основанный на нашем опыте. Здесь мы расскажем, как заработать деньги эффективно и быстро.\n"
        "🔓 Мы публикуем бесплатные мануалы три раза в неделю, а также у нас можно приобрести расширенные мануалы и всё, что требуется для комфортной работы.\n"
        "🖇️ По всем остальным вопросам – @silversssteams"
    )
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]
    ])
    
    await send_or_edit_photo(callback, "info", caption, keyboard)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "cooperation")
async def show_cooperation(callback: types.CallbackQuery):
    caption = (
        "💸 Сотрудничество создано для продвижения ваших проектов.\n\n"
        "🖇️ По вопросам размещения рекламы или другим вопросам обращайтесь @silversssteams."
    )
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]
    ])
    
    await send_or_edit_photo(callback, "cooperation", caption, keyboard)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "themes")
async def show_themes(callback: types.CallbackQuery):
    caption = (
        "⚖️ Переход в канал платный, но оправдает все ваши траты. За небольшую плату вы получите тонну полезной информации для заработка.\n\n"
        "⚔️ На данный момент система оплаты находится в разработке. Для покупки обращайтесь к администратору – @silversssteams."
    )
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]
    ])
    
    await send_or_edit_photo(callback, "themes", caption, keyboard)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "back_main")
async def back_main(callback: types.CallbackQuery):
    try:
        if os.path.exists(IMAGE_PATHS["main"]):
            with open(IMAGE_PATHS["main"], 'rb') as file:
                photo_data = file.read()
            
            await callback.message.edit_media(
                media=types.InputMediaPhoto(
                    media=BufferedInputFile(photo_data, filename="main.jpg"),
                    caption="Добро пожаловать! Выберите раздел:"
                ),
                reply_markup=get_main_menu_keyboard()
            )
        else:
            await callback.message.edit_caption(
                caption="Добро пожаловать! Выберите раздел:",
                reply_markup=get_main_menu_keyboard()
            )
            
    except Exception as e:
        logger.error(f"Ошибка возврата: {e}")
        await callback.answer()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    os.makedirs("images", exist_ok=True)
    asyncio.run(main())