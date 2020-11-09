import os
import logging 

from time import sleep
from collections import defaultdict

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from cutter import cut_file, DEFAULT_CHUNK_DURATION, DEFAULT_THRESHOLD

TOKEN = ''

chunk_configs = dict()
threshold_configs = dict()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    chat_id = update.effective_chat.id
    msg = 'Olá, mande um áudio com muitas pausas que eu corto pra você. Se precisar de ajuda digite /help.'
    context.bot.send_message(chat_id=chat_id, text=msg)

def help(update, context):
    chat_id = update.effective_chat.id

    msg = 'Ajuda é pra otário'
    context.bot.send_message(chat_id=chat_id, text=msg)

    sleep(1)

    msg = 'Brincadeira'
    context.bot.send_message(chat_id=chat_id, text=msg)

    msg = '/help - Mostrar essa mensagem (hur dur). \n'
    msg += '/chunk arg - Ajusta o intervalo mínimo de silêncio. \n'
    msg += '/threshold arg - Ajusta o volume mínimo para cortar. \n'
    context.bot.send_message(chat_id=chat_id, text=msg)

def chunk(update, context):
    try:
        chat_id = update.effective_chat.id
        chunk_duration = float(context.args[0])
        chunk_configs[chat_id] = chunk_duration  
        msg = f'Intervalo mínimo de silêncio alterado para {chunk_duration}.'
        update.message.reply_text(msg)
    except:
        msg = f'Formato inválido. Para mudar o parâmetro Chunk escreva algo como "/chunk {DEFAULT_CHUNK_DURATION}".'
        update.message.reply_text(msg)
    
def threshold(update, context):
    try:
        chat_id = update.effective_chat.id
        threshold = float(context.args[0])
        threshold_configs[chat_id] = threshold  
        msg = f'Volume mínimo alterado para {threshold}'
        update.message.reply_text(msg)
        print(msg, '\n')
    except:
        msg = f'Formato inválido. Para mudar o parâmetro Threshold escreva algo como "/threshold {DEFAULT_THRESHOLD}".'
        update.message.reply_text(msg)
    
def voice(update, context):
    chat_id = update.effective_chat.id
    file_id = update.effective_message.voice.file_id
    file_info = context.bot.get_file(file_id)

    original_file_path = 'movies/' + file_id + '.oga'
    edited_file_path = 'movies/' + file_id + '_edited' + '.mp3'

    chunk_duration = chunk_configs[chat_id] if (chat_id in chunk_configs) else DEFAULT_CHUNK_DURATION
    threshold = threshold_configs[chat_id] if (chat_id in threshold_configs) else DEFAULT_THRESHOLD

    file_info.download(original_file_path)
    cut_file(original_file_path, edited_file_path, chunk_duration, threshold)

    context.bot.send_voice(chat_id=chat_id, voice=open(edited_file_path, 'rb'))

    os.remove(original_file_path)
    os.remove(edited_file_path)

def audio(update, context):
    chat_id = update.effective_chat.id
    file_id = update.effective_message.audio.file_id
    file_info = context.bot.get_file(file_id)

    _, extension = os.path.splitext(file_info.file_path)
    original_file_path = 'movies/' + file_id + extension
    edited_file_path = 'movies/' + file_id + '_edited' + '.mp3'

    chunk_duration = chunk_configs[chat_id] if (chat_id in chunk_configs) else DEFAULT_CHUNK_DURATION
    threshold = threshold_configs[chat_id] if (chat_id in threshold_configs) else DEFAULT_THRESHOLD

    file_info.download(original_file_path)
    cut_file(original_file_path, edited_file_path, chunk_duration, threshold)

    context.bot.send_audio(chat_id=chat_id, audio=open(edited_file_path, 'rb'), title='audio.mp3')
    os.remove(original_file_path)
    os.remove(edited_file_path)

def video(update, context):
    chat_id = update.effective_chat.id
    file_id = update.effective_message.video.file_id
    file_info = context.bot.get_file(file_id)

    _, extension = os.path.splitext(file_info.file_path)
    original_file_path = 'movies/' + file_id + extension
    edited_file_path = 'movies/' + file_id + '_edited' + '.mp4'

    chunk_duration = chunk_configs[chat_id] if (chat_id in chunk_configs) else DEFAULT_CHUNK_DURATION
    threshold = threshold_configs[chat_id] if (chat_id in threshold_configs) else DEFAULT_THRESHOLD

    file_info.download(original_file_path)
    cut_file(original_file_path, edited_file_path, chunk_duration, threshold)

    context.bot.send_video(chat_id=chat_id, video=open(edited_file_path, 'rb'))
    os.remove(original_file_path)
    os.remove(edited_file_path)


def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('chunk', chunk))
    dp.add_handler(CommandHandler('threshold', threshold))

    dp.add_handler(MessageHandler(Filters.voice, voice))
    dp.add_handler(MessageHandler(Filters.audio, audio))
    dp.add_handler(MessageHandler(Filters.video, video))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()