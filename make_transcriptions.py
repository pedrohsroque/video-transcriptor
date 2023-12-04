import os

def make_transcription(video_filename):
    transcriptions_folder = f"transcriptions/{video_filename}"
    lines = []
    for file in os.listdir(transcriptions_folder):
        with open(f"{transcriptions_folder}/{file}","r", encoding="utf-8") as f:
            lines.append(f.read())
    with open(f"{transcriptions_folder}.txt","w", encoding="utf-8") as f:
        # f.writelines(lines)
        for line in lines:
            f.write(line+'\n')

if __name__ == "__main__":
    video_filename = input("video filename: ")
    make_transcription(video_filename)
