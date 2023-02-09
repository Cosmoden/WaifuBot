import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import TOKEN
from waifuim import WaifuAioClient

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
updater = None
tags = ['maid', 'waifu', 'oppai', 'selfies', 'uniform', 'mori-calliope', 'marin-kitagawa', 'raiden-shogun', 'ass',
        'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero']


async def start(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Начинаем работу."
    )


async def new_member(update, context):
    for member in update.message.new_chat_members:
        if member.username == 'WaifuBot':
            await context.bot.send_message(hat_id=update.effective_chat.id,
                                           text='Всем привет! Надеюсь, мы хорошо проведем время')


async def bot_help(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='''Этот бот может присылать случайные арты по тегам \n
    Напишите команду /image, а после нее - желаемые теги через пробел, например /image maid oppai \n
    Обычные теги:
    maid 
    waifu 
    oppai 
    selfies 
    uniform 
    mori-calliope 
    marin-kitagawa 
    raiden-shogun \n
    NSFW теги:
    ass 
    hentai 
    milf 
    oral 
    paizuri 
    ecchi
    ero''')


async def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


async def image(update, context):
    wf = WaifuAioClient()
    for arg in context.args:
        if arg not in tags:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Неизвестный тег")
            return
    res = await wf.search(included_tags=context.args)
    await wf.close()
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=str(res))


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', bot_help))
    app.add_handler(CommandHandler('image', image))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    app.add_error_handler(error)
    app.run_polling()
