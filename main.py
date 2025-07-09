import csv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from io import StringIO

questions = [
]

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def send_question(update_or_callback, context):
    pass

def evaluate_level(score, total):
    pass

async def handle_answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def finish_test(update, context):
    pass


if __name__ == '__main__':
    print("Bot is running...")

