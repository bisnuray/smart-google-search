"""
Author: Bisnu Ray
Telegram: https://t.me/SmartBisnuBio
"""

import os
import requests
import time
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import CantParseEntities
from aiogram.types import InputMediaPhoto

# BOT TOKEN
BOT_TOKEN = 'telegram_bot_token'  # <-- Replace this with your actual bot token

# Initialization
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# User cooldowns and admin_ids
user_cooldowns = {}
admin_ids = [123456, 123456]  # Replace with your admin IDs

def on_cooldown(user_id):
    cooldown_time = 600  # 10 minutes in seconds
    if user_id in user_cooldowns:
        last_used_time = user_cooldowns[user_id]
        if time.time() - last_used_time < cooldown_time:
            return True
    return False

# Google search configuration
GOOGLE_API_KEY = 'abcdefgh' #GOOGLE_API_KEY
GOOGLE_CSE_ID = 'abcdefg' #GOOGLE_CSE_ID
RESULTS_PER_PAGE = 5

async def send_search_results(bot, chat_id, message_id, query, start_index, search_type='text'):
    search_url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}&q={query}&start={start_index}&num={RESULTS_PER_PAGE}"
    
    if search_type == 'image':
        search_url += "&searchType=image"

    response = requests.get(search_url)
    search_results = response.json()

    if 'items' in search_results:
        if search_type == 'image':
            media_group = []
            for i, item in enumerate(search_results['items'], start=start_index):
                try:
                    media = InputMediaPhoto(media=item['link'], caption=f"{i}. [Image]({item['link']})", parse_mode=types.ParseMode.MARKDOWN)
                    media_group.append(media)
                except:
                    continue

            if media_group:
                await bot.send_media_group(chat_id, media=media_group)
            else:
                await bot.edit_message_text("No images found.", chat_id, message_id)
        else:
            result_message = "<b>Your Search results:</b>\n\n"
            for i, item in enumerate(search_results['items'], start=start_index):
                description = item.get('snippet', 'No description available.')
                result_message += f"{i}. <b>[{item['title']}]</b>{item['link']}\n{description}\n\n"

            keyboard = InlineKeyboardMarkup()
            buttons = []

            if start_index > 1:
                buttons.append(InlineKeyboardButton("Previous", callback_data=f"prev_{query}_{start_index}_{search_type}"))

            if 'queries' in search_results and 'nextPage' in search_results['queries']:
                buttons.append(InlineKeyboardButton("Next", callback_data=f"next_{query}_{start_index}_{search_type}"))

            keyboard.row(*buttons)
            
            await bot.edit_message_text(result_message, chat_id, message_id, parse_mode=types.ParseMode.HTML, reply_markup=keyboard, disable_web_page_preview=True)
    else:
        await bot.edit_message_text("No results found.", chat_id, message_id)

async def search(message, bot):
    command, query = message.text.split(maxsplit=1)
    if command in ['/image', '.image']:
        search_type = 'image'
    else:
        search_type = 'text'

    user_id = message.from_user.id

    if search_type == 'image' and user_id not in admin_ids:
        if on_cooldown(user_id):
            await message.reply("You can use the /image command once every 10 minutes. Please wait.")
            return
        else:
            # Update the user's last used time
            user_cooldowns[user_id] = time.time()

    if query:
        sent_message = await message.reply("<b>Searching... Please wait.</b>", parse_mode=types.ParseMode.HTML)
        try:
            search_results_message = await send_search_results(bot, message.chat.id, sent_message.message_id, query, 1, search_type)
        except CantParseEntities:
            search_results_message = await message.reply("<b>⚠️ Google SafeSearch is on, so no results</b>", parse_mode=types.ParseMode.HTML)
        
    else:
        await message.reply("Please provide a search query after the command.")

async def process_callback_query(callback_query, bot):
    action, query, start_index, search_type = callback_query.data.split('_')
    start_index = int(start_index)

    if action == 'next':
        start_index += RESULTS_PER_PAGE
    else:
        start_index -= RESULTS_PER_PAGE

    await bot.answer_callback_query(callback_query.id)
    await send_search_results(bot, callback_query.message.chat.id, callback_query.message.message_id, query, start_index, search_type)

@dp.message_handler(commands=['search', 'image'])
async def handle_search(message: types.Message):
    await search(message, bot)

@dp.callback_query_handler(lambda c: c.data.startswith('prev_') or c.data.startswith('next_'))
async def handle_callback(callback_query: types.CallbackQuery):
    await process_callback_query(callback_query, bot)

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
