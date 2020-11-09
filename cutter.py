import os
import numpy as np

from time import time

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import concatenate_audioclips
from moviepy.video.compositing.concatenate import concatenate_videoclips

VIDEO_FORMATS = ['.mp4', '.mpeg']
AUDIO_FORMATS = ['.mp3', '.oga']

DEFAULT_THRESHOLD = 0.05
DEFAULT_CHUNK_DURATION = 0.5

def get_loud_timings(audio_clip, chunk_duration=DEFAULT_CHUNK_DURATION, threshold=DEFAULT_THRESHOLD):  
    loud_timings = []
    chunks = audio_clip.iter_chunks(chunk_duration=chunk_duration)

    silence_section = True
    
    for i, chunk in enumerate(chunks):
        loud_sound = np.max(chunk) >= threshold

        if silence_section and loud_sound: 
            start_sound = i*chunk_duration
            silence_section = False 

        elif not (silence_section or loud_sound):
            end_sound = i*chunk_duration
            silence_section = True
            loud_timings.append((start_sound, end_sound))

    if not silence_section:
        loud_timings.append((start_sound, audio_clip.duration))
    
    return loud_timings or [(0, .1)]


def cut_audio_silence(audio_clip, chunk_duration=DEFAULT_CHUNK_DURATION, threshold=DEFAULT_THRESHOLD):
    loud_timings = get_loud_timings(audio_clip, chunk_duration, threshold)
    loud_sections = [audio_clip.subclip(start, end) for start, end in loud_timings]
    return concatenate_audioclips(loud_sections)

def cut_video_silence(video_clip, chunk_duration=DEFAULT_CHUNK_DURATION, threshold=DEFAULT_THRESHOLD):
    loud_timings = get_loud_timings(video_clip.audio, chunk_duration, threshold)
    loud_sections = [video_clip.subclip(start, end) for start, end in loud_timings]
    return concatenate_videoclips(loud_sections)

def cut_file(input_file, output_file, chunk_duration=DEFAULT_CHUNK_DURATION, threshold=DEFAULT_THRESHOLD):
    if not os.path.exists(input_file):
        raise FileNotFoundError()

    filename, extension = os.path.splitext(input_file)

    if extension in VIDEO_FORMATS:
        original = VideoFileClip(input_file)
        eddited = cut_video_silence(original, chunk_duration, threshold)
        eddited.write_videofile(output_file, logger=None)
    elif extension in AUDIO_FORMATS:
        original = AudioFileClip(input_file)
        eddited = cut_audio_silence(original, chunk_duration, threshold)
        eddited.write_audiofile(output_file, logger=None)
    else:
        raise OSError('File format not supported') 


if __name__ == '__main__':
    start = time()
    cut_file('teste.oga', 'edited.mp3')
    end = time()
    print(end-start)
