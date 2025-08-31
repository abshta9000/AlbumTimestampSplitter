import random
import csv
import subprocess
from pathlib import Path
from datetime import timedelta
import json
import os
import eyed3

FILE_PREFIX = r"F:\Code\splitter\EA2 CD-0"
OUTPUT_DIR = Path("clips")
TRACKLIST_PATH = 'tracklist.json'

def get_video_duration(filename):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json", filename
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])


file_paths = [os.path.join(os.getcwd(), file) for file in os.listdir(os.getcwd()) if file.endswith(".mp3")]

with open(TRACKLIST_PATH, 'r') as file:
    tracklist = json.load(file)  

timestamps = []
for song in tracklist:
    minutes,seconds = song["duration"].split(":")    
    disc,track = song["trackPos"].split("-")
    timestamps.append([timedelta(minutes=int(minutes),seconds=int(seconds)),disc,track,song["artist"],song["title"],song["comments"]])

OUTPUT_DIR.mkdir(exist_ok=True)

current_start = 0  
current_file = 1

num="b"

for i, timestamp in enumerate(timestamps):

    if current_file != timestamp[1]:
        current_file = timestamp[1]
        current_start = 0

    duration = timestamp[0].seconds
    output_name = str(num) + ".mp3"
    num+="b"
    output_path = OUTPUT_DIR / output_name

    command = [
        "ffmpeg",
        "-ss", str(current_start),
        "-i", FILE_PREFIX + str(current_file) + ".mp3",
        "-map", "0",              
        "-map_metadata", "0",     
        "-map_metadata", "0:s:0",
        "-c:a", "libmp3lame",     
        "-q:a", "2",
        "-id3v2_version", "3",     
        "-vn"
    ]

    try:
        if timestamps[i+1][1] == timestamps[i][1]:
            command.extend(["-t", str(duration)])
    except IndexError:
        ""

    command.append(str(output_path))

    print("Running:", " ".join(command))
    subprocess.run(command, check=True)
    audiofile = eyed3.load(output_path)
    audiofile.tag.disc_num = timestamp[1]
    audiofile.tag.track_num  = timestamp[2]
    audiofile.tag.artist = timestamp[3]
    audiofile.tag.title = timestamp[4]
    audiofile.tag.comments.set(timestamp[5])
    audiofile.tag.save()

    current_start += int(duration)

print("✅ All clips exported!")