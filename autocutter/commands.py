import logging 
from time import sleep
from pathlib import Path
from telegram.ext import CommandHandler, MessageHandler, Filters

from config import TEMP_PATH, DB_PATH
from database import DataBase
from cutter import cut_file, VIDEO_FORMATS, AUDIO_FORMATS

DEFAULT_THRESHOLD = 0.05
DEFAULT_CHUNK_DURATION = 0.2
DB = DataBase(DB_PATH)

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
        '/set_chunk arg - Ajusta o intervalo mínimo de silêncio. \n'
        '/set_threshold arg - Ajusta o volume mínimo. \n'
        '/get_chunk - Verifica o intervalo mínimo de silêncio atual. \n'
        '/get_threshold - Verifica o volume mínimo atual. \n'
        '/restart_configs - Restaura as definições padrão de volume e intervalo. \n'
    )

def set_chunk(update, context):
    chat = update.effective_chat
    message = update.effective_message
    try:
        chunk_duration = float(context.args[0])
        new_user = DB.find_user(chat.id) is None
        if new_user:
            DB.add_user(chat.id, chunk_duration, DEFAULT_THRESHOLD)
        else:
            DB.update_chunk(chat.id, chunk_duration)
        message.reply_text(f'Intervalo mínimo de silêncio alterado para {chunk_duration}.')

    except ValueError:
        message.reply_text(f'Formato inválido. Para mudar o parâmetro Chunk escreva algo como "/set_chunk {DEFAULT_CHUNK_DURATION}".')
    
def set_threshold(update, context):
    chat = update.effective_chat
    message = update.effective_message
    try:
        threshold = float(context.args[0])
        new_user = DB.find_user(chat.id) is None
        if new_user:
            DB.add_user(chat.id, DEFAULT_CHUNK_DURATION, threshold)
        else:
            DB.update_threshold(chat.id, threshold)
        message.reply_text(f'Volume mínimo alterado para {threshold}.')

    except ValueError:
        message.reply_text(f'Formato inválido. Para mudar o parâmetro Threshold escreva algo como "/set_theshold {DEFAULT_THRESHOLD}".')

def restart_configs(update, context):
    chat = update.effective_chat
    DB.remove_user(chat.id)
    chat.send_message('Configurações restauradas')

def get_chunk(update, context):
    chat = update.effective_chat
    user = DB.find_user(chat.id)
    chunk = DEFAULT_CHUNK_DURATION if (user is None) else user[1]
    chat.send_message(chunk)

def get_threshold(update, context):
    chat = update.effective_chat
    user = DB.find_user(chat.id)
    threshold = DEFAULT_THRESHOLD if (user is None) else user[2]
    chat.send_message(threshold)
    
def remove_silence(update, context):
    chat = update.effective_chat
    message = update.effective_message
    data = message.voice or message.audio or message.video
    file = data.get_file()

    input_ext = Path(file.file_path).suffix

    if input_ext in AUDIO_FORMATS:
        output_ext = '.mp3'
    elif input_ext in VIDEO_FORMATS:
        output_ext = '.mp4'
    else:
        raise OSError('File format not supported') 
    
    input_file_path = TEMP_PATH / (data.file_id + input_ext)
    output_file_path = TEMP_PATH / (data.file_id + output_ext)

    user = DB.find_user(chat.id)
    _, chunk, threshold = user if (user is not None) else (None, DEFAULT_CHUNK_DURATION, DEFAULT_THRESHOLD)
    
    file.download(input_file_path.as_posix())
    cut_file(input_file_path, output_file_path, chunk, threshold)

    if message.voice is not None:
        chat.send_voice(open(output_file_path, 'rb'))
    elif message.audio is not None:
        chat.send_audio(open(output_file_path, 'rb'))
    elif message.video is not None:
        chat.send_video(open(output_file_path, 'rb'))
    else:
        raise OSError('File format not supported') 

    input_file_path.unlink()
    output_file_path.unlink()


HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('help', help),
    CommandHandler('set_chunk', set_chunk),
    CommandHandler('set_threshold', set_threshold),
    CommandHandler('get_chunk', get_chunk),
    CommandHandler('get_threshold', get_threshold),
    CommandHandler('restart_configs', restart_configs),
    MessageHandler(Filters.voice | Filters.audio | Filters.video, remove_silence),
]
