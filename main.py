import os
import sys
import json
import random
from os.path import isfile, join
from pathlib import Path

# ffmpeg_bin = '/usr/local/bin/ffmpeg'
# ffmpeg_bin = '/usr/bin/ffmpeg'
ffmpeg_bin = 'ffmpeg'


def main(arguments):
    file = open("settings.json", "r")
    json_string = file.read()
    settings = json.loads(json_string)
    album = settings['album']
    artist = settings['artist']
    year = settings['year']
    audio_path = str(Path.home()) + settings['audio_path']
    cover_path = str(Path.home()) + settings['cover_path']
    output_path = str(Path.home()) + settings['output_path']
    if len(arguments) > 0:
        for argument in arguments[1:]:
            key, value = argument.split('=', 1)
            if key == "album":
                album = value
            elif key == "artist":
                artist = value
            elif key == "year":
                year = value
            elif key == "cover_path":
                cover_path = value
            elif key == "output_path":
                output_path = value
            elif key == "audio_path":
                audio_path = value

    audio_files = [f for f in os.listdir(audio_path) if isfile(join(audio_path, f))]
    cover_files = [f for f in os.listdir(cover_path) if isfile(join(cover_path, f)) and (
                f.lower().endswith(".png") or f.lower().endswith('.jpg') or f.lower().endswith('.jpeg'))]
    track = 0
    for file in audio_files:
        track = audio_files.index(file)
        length = len(file)
        title = file[:length - 4]
        path = audio_path + file
        pic = cover_path + cover_files[random.randrange(0, len(cover_files))]
        music_output_path = output_path + title
        track = track + 1

        ffmpeg = "{} -i \"{}\" -i \"{}\" -map 0:0 -map 1:0 -codec:v copy -codec:a libmp3lame -q:a 2  -id3v2_version 4 " \
                 "-metadata title=\"{}\" " \
                 "-metadata artist=\"{}\" " \
                 "-metadata album_artist=\"{}\" " \
                 "-metadata album=\"{}\" " \
                 "-metadata genre=\"Hip-Hop/Rap\" " \
                 "-metadata year={} " \
                 "-metadata track={} " \
                 "\"{}.mp3\"".format(ffmpeg_bin, path, pic, title, artist, artist, album, year, track,
                                     music_output_path)

        print(ffmpeg)
        os.system(ffmpeg)


args = sys.argv
main(args)
