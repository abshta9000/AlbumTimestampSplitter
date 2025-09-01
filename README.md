# Album Timestamp Splitter
A simple python script that takes a full mp3 album and splits it based on timestamp data. Titles and artists are added to the splitted songs and previous metadata is preserved, such as album art. **MP3s are *ONLY* supported**
## Installation and Usage
This script uses these libraries and programs:
- FFMpeg
  * This splits the mp3s cleanly whilst preserving metadata
  * Make sure `ffmpeg` is added to your path
- mutagen
  * For actually editing the ID3 data
- pathvalidate
  * Makes sure title names don't contain any strange characters that can cause file errors

You can install `mutagen` and `pathvalidate` with this `pip` command:

```python -m pip install mutagen pathvalidate```

To actually get the JSON tracklist, run the Tampermonkey script for Discogs (effective September 2025), or alternatively use the example JSON listed and match it you your data.
## Limitations
- Only works with MP3s
- Discs must be split into seperate audio files and different discs must have the same file prefix

It's a very, very simple script so I recommend actually looking through and modifying anything you don't like.
