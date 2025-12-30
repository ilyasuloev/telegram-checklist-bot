import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8405014883:AAFqXTQcXuLYmurfBucI_4ml8vzHtkahtAo")
CHANNEL_ID = -1001679517849

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== КЛАВИАТУРЫ ==========
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Получить чек-лист", callback_data="get_checklist")]
    ])
    return keyboard

def get_channel_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться на канал", url="https://t.me/small_step_first")],
        [InlineKeyboardButton(text="✅ Я подписался", callback_data="check_subscription")]
    ])
    return keyboard

# ========== ПРОВЕРКА ПОДПИСКИ ==========
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status not in ["left", "kicked"]:
            return True
        return False
    except Exception as e:
        logger.error(f"Ошибка проверки: {e}")
        return False

# ========== ОБРАБОТЧИКИ ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = """Привет!
Я подготовил для тебя бесплатный чек-лист
«7 правил здоровья, энергии и продуктивности».

Чтобы его получить:
— подпишись на мой канал 👇
@small_step_first

И нажми "Я подписался\""""
    
    await message.answer(text, reply_markup=get_main_keyboard())
    logger.info(f"Пользователь {message.from_user.id} запустил бота")

@dp.callback_query(lambda c: c.data == "get_checklist")
async def process_checklist(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    await callback.message.edit_text("⏳ Проверяю подписку...")
    
    is_subscribed = await check_subscription(user_id)
    
    if is_subscribed:
        await asyncio.sleep(1)
        await callback.message.edit_text("✅ Подписка подтверждена!")
        await asyncio.sleep(1)
        
        checklist_text = """Вот обещанный чек-лист
«7 правил здоровья, энергии и продуктивности».

Забирай 👇
https://disk.yandex.ru/i/xqvFaV_yeEqtjg

Больше лайва в моем Inst: 
https://www.instagram.com/ilyasuloev?igsh=NmMzcHowYmh4eGUw&utm_source=qr"""
        
        await bot.send_message(user_id, checklist_text)
        logger.info(f"Пользователь {user_id} получил чек-лист")
    else:
        text = """Привет!
Я подготовил для тебя бесплатный чек-лист
«7 правил здоровья, энергии и продуктивности».

Чтобы его получить:
— подпишись на мой канал 👇
@small_step_first

И нажми кнопку ниже👇"""
        
        await callback.message.edit_text(text, reply_markup=get_channel_keyboard())
    
    await callback.answer()

@dp.callback_query(lambda c: c.data == "check_subscription")
async def check_subscription_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    await callback.message.edit_text("⏳ Проверяю...")
    
    is_subscribed = await check_subscription(user_id)
    
    if is_subscribed:
        await asyncio.sleep(1)
        await callback.message.edit_text("✅ Отлично! Вы подписаны!")
        await asyncio.sleep(1)
        
        checklist_text = """Вот обещанный чек-лист
«7 правил здоровья, энергии и продуктивности».

Забирай 👇
https://disk.yandex.ru/i/xqvFaV_yeEqtjg

Больше лайва в моем Inst: 
https://www.instagram.com/ilyasuloev?igsh=NmMzcHowYmh4eGUw&utm_source=qr"""
        
        await bot.send_message(user_id, checklist_text)
        logger.info(f"Пользователь {user_id} подписался и получил чек-лист")
    else:
        await callback.message.edit_text(
            "❌ Вы еще не подписаны!\n\n"
            "Подпишитесь на канал @small_step_first\n"
            "и нажмите кнопку еще раз👇",
            reply_markup=get_channel_keyboard()
        )
    
    await callback.answer()

@dp.message()
async def any_message(message: types.Message):
    if message.text and not message.text.startswith('/'):
        await message.answer(
            "Напишите /start чтобы начать",
            reply_markup=get_main_keyboard()
        )

# ========== ЗАПУСК БОТА ==========
async def main():
    logger.info("=" * 50)
    logger.info("🤖 ТЕЛЕГРАМ БОТ ЗАПУЩЕН НА KOYEB!")
    logger.info("📢 Канал: @small_step_first")
    logger.info("=" * 50)
    
    try:
        bot_info = await bot.get_me()
        logger.info(f"✅ Бот: @{bot_info.username}")
        logger.info(f"✅ Имя: {bot_info.first_name}")
        logger.info("✅ Бот готов к работе 24/7!")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения: {e}")
        return
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
