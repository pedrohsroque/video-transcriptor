import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.editor as mp
import speech_recognition as sr

from make_transcriptions import make_transcription

def extract_audio(video_path, audio_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_duration = audio_clip.duration
    audio_clip.write_audiofile(audio_path)
    audio_clip.close()
    return audio_duration

def split_and_save_audio(video_path):
    new_folder = f"audios/{video_filename}"
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    interval_size = 15
    audio_duration = audio_clip.duration
    for start_time in range(0, int(audio_duration), interval_size):
        start_time_improved = start_time if start_time == 0 else start_time - 3
        end_time = min(start_time + interval_size, audio_duration)
        audio_segment = audio_clip.subclip(start_time_improved, end_time)
        output_file = f"audios/{video_filename}/audio_part_{str(start_time).zfill(4)}.wav"
        audio_segment.write_audiofile(output_file)
    video_clip.close()
    audio_clip.close()

def transcribe_audio(audio_path: str):
    print(f"Transcrevendo {audio_path}")
    new_folder = f"transcriptions/{video_filename}"
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    filename = audio_path.split('/')[-1].split('.')[0]
    transcription_path = f"{new_folder}/{filename}.txt"
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)
    
    with audio_file as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language="en-US")
        with open(transcription_path, "w", encoding='utf-8') as f:
            f.write(text)
    except sr.UnknownValueError:
        return "Não foi possível reconhecer o áudio"
    except sr.RequestError as e:
        return f"Erro na requisição ao serviço de reconhecimento de fala: {e}"

video_filename = input("Video filename (without extension): ")

video_path = f"videos/{video_filename}.mp4"

audio_path = f"audios/{video_filename}/{video_filename}.wav"

split_and_save_audio(video_path)

audio_folder = f"audios/{video_filename}"
for file in os.listdir(f"audios/{video_filename}"):
    transcribe_audio(f"{audio_folder}/{file}")

make_transcription(video_filename)
