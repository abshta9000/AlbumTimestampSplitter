import random
import csv
import subprocess
from pathlib import Path
from datetime import timedelta
import json
import os
from mutagen.easyid3 import EasyID3
import pathvalidate

FILE_PREFIX = r"F:\Code\splitter\EA2 CD-0"
OUTPUT_DIR = Path("clips")
TRACKLIST_PATH = 'tracklist.json'
ALBUM_NAME = "Electronic Architechture 2"

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
    timestamps.append({
        "duration": timedelta(minutes=int(minutes),seconds=int(seconds)),
        "disc":     int(disc),
        "track":    int(track),
        "artist":   song["artist"],
        "title":    song["title"],
        "comments": song["comments"]
    })

OUTPUT_DIR.mkdir(exist_ok=True)
while (True):
    confirmation = input("Everything in " + str(OUTPUT_DIR) + " is getting deleted. Do you want to continue? [y/N] ")
    if confirmation.upper() in ["Y", "N", ""]:
        input = confirmation
        break
if input.upper() in ["Y", ""]:
    for file_name in os.listdir(OUTPUT_DIR):
        file_path = os.path.join(OUTPUT_DIR, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
elif input.upper() in ["N", ""]:
    Exception("Operation cancelled by user. No files were deleted.")

current_start = 0  
current_disc = 1

num="b"

for i, timestamp in enumerate(timestamps):
    print("⏭️ Now Starting: " + timestamp["title"])

    if current_disc != timestamp["disc"]:
        current_disc = timestamp["disc"]
        current_start = 0

    duration = timestamp["duration"].seconds
    output_name = pathvalidate.sanitize_filename(f"[{random.randint(10000,99999)}] " + timestamp["title"] + ".mp3")
    output_path = OUTPUT_DIR / output_name

    command = [
        "ffmpeg",
        "-ss", str(current_start),
        "-i", FILE_PREFIX + str(current_disc) + ".mp3",
        "-map", "0:a",           
        "-map", "0:v?",          
        "-map_metadata", "0",    
        "-c:a", "libmp3lame",    
        "-q:a", "2",
        "-c:v", "copy",          
        "-id3v2_version", "3",
        "-write_id3v2", "1"
    ]

    try:
        if timestamps[i+1]["disc"] == timestamps[i]["disc"]:
            command.extend(["-t", str(duration)])
    except IndexError:
        ""

    command.append(str(output_path))

    print("Running:", " ".join(command))
    subprocess.run(command, check=True)

    EasyID3.RegisterTextKey('comment', 'COMM')
    tags = EasyID3(output_path)
    tags["title"] = timestamp["title"]
    tags["artist"] = timestamp["artist"]
    tags["album"] = ALBUM_NAME
    tags["tracknumber"] = str(timestamp["track"])
    tags["discnumber"] = str(timestamp["disc"])
    tags["comment"] = timestamp["comments"]
    tags.save(v2_version=3)


    current_start += int(duration)
    print("☑️ Successfully finished: " + timestamp["title"])

print("✅ All clips exported!")