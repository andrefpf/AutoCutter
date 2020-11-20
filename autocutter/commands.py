import os
import logging 
from time import sleep
from telegram.ext import CommandHandler, MessageHandler, Filters

from cutter import cut_file, DEFAULT_CHUNK_DURATION, DEFAULT_THRESHOLD

chunk_configs = dict()
threshold_configs = dict()

def start(update, context):
    chat = update.effective_chat
    print(chat.id)
    chat.send_message(
        'Olá, mande um áudio com muitas pausas que eu corto pra você. Se precisar de ajuda digite /help.'
    )

def help(update, context):
    chat = update.effective_chat
    chat.send_message('Ajuda é pra otário')
    sleep(1)
    chat.send_message('Brincadeira')
    chat.send_message(
        '/help - Mostrar essa mensagem (hur dur). \n'
        '/chunk arg - Ajusta o intervalo mínimo de silêncio. \n'
        '/threshold arg - Ajusta o volume mínimo para cortar. \n'
    )

def chunk(update, context):
    try:
        chat = update.effective_chat
        chunk_duration = float(context.args[0])
        chunk_configs[chat.id] = chunk_duration  
        update.message.reply_text(f'Intervalo mínimo de silêncio alterado para {chunk_duration}.')
    except:
        update.message.reply_text(
            'Formato inválido.'
           f'Para mudar o parâmetro Chunk escreva algo como "/chunk {DEFAULT_CHUNK_DURATION}".'
        )
    
def threshold(update, context):
    try:
        chat = update.effective_chat
        threshold = float(context.args[0])
        threshold_configs[chat_id] = threshold
        update.message.reply_text(f'Volume mínimo alterado para {threshold}')
    except:
        update.message.reply_text(
            'Formato inválido.'
           f'Para mudar o parâmetro Threshold escreva algo como "/threshold {DEFAULT_THRESHOLD}".'
        )
    
def voice(update, context):
    chat_id = update.effective_chat.id
    file_id = update.effective_message.voice.file_id
    file_info = context.bot.get_file(file_id)

    print((update.effective_message.audio))

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


HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('help', help),
    CommandHandler('chunk', chunk),
    CommandHandler('threshold', threshold),
    MessageHandler(Filters.voice, voice),
    MessageHandler(Filters.audio, audio),
    MessageHandler(Filters.video, video),
]