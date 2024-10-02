#!/usr/local/bin/bash
#
# Change the sample rate (audio rate) of a WAV file using https://ffmpeg.org/
#
# Usage: resample.sh file.wav [file2.wav ...]
# For example: resample.sh *.wav
#
set -ueo pipefail

SAMPLE_RATE=48000

for source_file in "$@"
do
  dest_file="${source_file%%.*}_${SAMPLE_RATE}.wav"
  echo "${source_file} -> ${dest_file}" 
  ffmpeg -loglevel warning -i $source_file -ar $SAMPLE_RATE $dest_file
done

