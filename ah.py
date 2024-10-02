#
# Selects the "ah" sound out of an audio file, and saves it as a mono WAV file.
#
# Requires a CSV file with a column for "Study Number" and "Start ah" (seconds).
# Expects a `Study NNN.m4a` file for each Study Number. 
#
import pandas as pd
import librosa
import soundfile as sf
import os
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Extract a 3-second segment of audio from each file listed in a CSV file')
parser.add_argument('csv_file', help='CSV file containing the list of files to process')
parser.add_argument('input_folder', help='Folder containing the input audio files')
parser.add_argument('output_folder', help='Folder to store the output files')
parser.add_argument('-d', '--duration', type=float, default=3.0, help='Duration of the audio segment (in seconds)')

args = parser.parse_args()

df = pd.read_csv(args.csv_file)
os.makedirs(args.output_folder, exist_ok=True)

def input_filename(studyNumber: str) -> str:
    # The input file is based on the study number but can be 3 or 4 digits with zero padding:
    possibilities = [
        os.path.join(args.input_folder, f'Study {studyNumber:03d}.m4a'),
        os.path.join(args.input_folder, f'Study {studyNumber:04d}.m4a')
    ]

    return next(filter(os.path.exists, possibilities), None)
            

for index, row in df.iterrows():
    if pd.isnull(row['Start ah']) or row['Start ah'] == '':
        print(f'Warning: "Start ah" value is missing for Study Number {row["Study Number"]}')
    else:
        studyNum = row['Study Number']
        input = input_filename(studyNum)

        # Outputs:
        fullWav = os.path.join(args.input_folder, f'Study {studyNum:04d}.wav')
        ahWav   = os.path.join(args.output_folder, f'ah Study {studyNum:04d} {args.duration} sec.wav')

        print(f"{input} -> {ahWav}")

        # Convert to mono WAV:
        if not os.path.exists(fullWav):
            subprocess.call(['ffmpeg', '-loglevel', 'warning', '-i', input, '-ac', '1', '-ar', '44100', fullWav])

        # Select "Ah" sound only
        audio, sr = librosa.load(fullWav, sr=None)
        start = int(sr * row['Start ah'])
        end = start + int(sr * args.duration)
        segment = audio[start:end]
        sf.write(ahWav, segment, sr)


