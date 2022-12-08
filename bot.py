import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)
from telegram import ForceReply, Update
from data_handler.xls_handler import read_excel_file


load_dotenv()

TOKEN = os.getenv("TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! \nplease send a xlsx file",
        reply_markup=ForceReply(selective=True),
    )


async def get_doc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get document"""
    await update.message.reply_html(
        "Let me think for a second"
    )
    try:
        os.mkdir('tmp/')
    except FileExistsError:
        pass
    file_id = update.message.document.file_id
    new_file = await context.bot.get_file(file_id)
    path = f'tmp/{file_id}'
    await new_file.download_to_drive(custom_path=path)
    values, mean_price = await read_excel_file(path)
    os.remove(path)
    await update.message.reply_html(
        f"I`ve got {len(values)} links from you:",
    )
    for value in values:
        await update.message.reply_html(
            f"name: {value[0]} \nusrl: {value[1]} \nxpath: {value[2]}",
        )
    await update.message.reply_html(
        f"The mean price is {mean_price}",
    )


def create_bot():
    """
    Create telegram bot application
    """
    bot_app = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )
    bot_app.add_handlers(
        handlers=[
            CommandHandler("start", start),
            MessageHandler(filters.ATTACHMENT, get_doc)
        ]
    )
    return bot_app


if __name__ == '__main__':
    bot_app = create_bot()
    bot_app.run_polling()
