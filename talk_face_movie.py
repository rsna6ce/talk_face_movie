#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess
import argparse
import wave
import numpy as np
import glob
from PIL import Image

def main():
    parser = argparse.ArgumentParser(prog='talk_face_movie.py')
    parser.add_argument('-i', '--input', help='input wav file', required=True, dest='input')
    parser.add_argument('-o', '--output', help='output mp4 file. default=(input).mp4', default='', dest='output')
    parser.add_argument('-f', '--frame_rate', help='frame_rate fps', default=15, dest='frame_rate')
    parser.add_argument('-p', '--picture_dir', help='directory of face picture', default='', type=str, dest='picture_dir')
    parser.add_argument('-s', '--small_threshold', help='small mouth sound threshold', default=0.1, type=float, dest='small_threshold')
    parser.add_argument('-l', '--large_threshold', help='large mouth sound threshold', default=0.25, type=float, dest='large_threshold')
    parser.add_argument('-b', '--blink_interval', help='blink interval (ms)', default=2000, type=int, dest='blink_interval')
    args = parser.parse_args()
    talk_face_movie(args)

def talk_face_movie(param):
    # clean up temp dir
    script_dir = os.path.dirname(__file__)
    temp_dir = script_dir + '/temp'
    for filename in  glob.glob(temp_dir + '/*.png'):
        os.remove(filename)

    # set picture dir
    picture_dir = script_dir + '/picture'
    if param.picture_dir != '':
        picture_dir = param.picture_dir
    #temp mp4
    temp_mp4 = script_dir + '/temp.mp4'

    filename_close = picture_dir + '/face_1.png'
    filename_small = picture_dir + '/face_2.png'
    filename_large = picture_dir + '/face_3.png'
    filename_blink = picture_dir + '/face_4.png'

    # read wav file param
    filename_input = param.input
    wave_file = wave.open(filename_input, 'r')
    wav_params = wave_file.getparams()
    #print(wav_params)

    # read wav file data
    wave_bin = wave_file.readframes(wave_file.getnframes())
    wave_nomal = np.frombuffer(wave_bin, dtype="int16") / (2**15-1) #signed int 16bit -> -1.0~1.0 nomalize

    # sample data loop
    data_length = len(wave_nomal)
    sample_interval = int(wav_params.framerate / param.frame_rate)
    sample_count = int(data_length / sample_interval)
    sample_count = 0
    signal_peak = 0
    latest_blink = 0
    frame_number = 0
    prev_style = ""
    for i in range(data_length):
        signal_peak = max(signal_peak, abs(wave_nomal[i]))
        sample_count += 1
        if sample_count >= sample_interval:
            frame_number_with_zero = str(frame_number).zfill(8)
            print("{}  {:.3f}".format(frame_number_with_zero, signal_peak), end='  ')
            temp_filename = temp_dir + '/' + frame_number_with_zero + '.png'
            frame_number += 1

            if signal_peak < param.small_threshold:
                if ((i - latest_blink)/wav_params.framerate) * 1000 > param.blink_interval:
                    latest_blink = i
                    # blink
                    shutil.copy(filename_blink, temp_filename)
                    prev_style = 'blink'
                    print('blink')
                else:
                    # close face
                    shutil.copy(filename_close, temp_filename)
                    prev_style = 'close'
                    print('close')
            elif signal_peak < param.large_threshold:
                # small mouth
                if prev_style == 'small':
                    # numnum
                    shutil.copy(filename_close, temp_filename)
                    prev_style = 'close'
                    print('close(small)')
                else:
                    shutil.copy(filename_small, temp_filename)
                    prev_style = 'small'
                    print('small')
            else:
                # large mouth
                if prev_style == 'large':
                    # numnum
                    shutil.copy(filename_small, temp_filename)
                    prev_style = 'small'
                    print('small(large)')
                else:
                    shutil.copy(filename_large, temp_filename)
                    prev_style = 'large'
                    print('large')
            sample_count = 0
            signal_peak = 0
    wave_file.close()

    # encode with ffmpeg
    frames_dir = temp_dir
    frame_rate = param.frame_rate
    img = Image.open(filename_close)
    width = img.width
    height = img.height
    img.close()
    subprocess.run(('ffmpeg' ,
        '-loglevel', 'warning',
        '-y',
        '-framerate', str(frame_rate),
        '-i', temp_dir+'/%8d.png',
        '-vframes', str(frame_number),
        '-vf', 'scale={0}:{1},format=yuv420p'.format(width, height),
        '-vcodec', 'libx264',
        '-r', str(frame_rate),
        temp_mp4))

    #mux sound with ffmpeg
    # ffmpeg -i 001.mp4 -i 001.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4 -y
    filename_output = param.output if param.output!='' else filename_input + '.mp4'
    subprocess.run(('ffmpeg' ,
        '-loglevel', 'warning',
        '-y',
        '-i', temp_mp4,
        '-i', param.input,
        '-c:v','copy',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '1:a:0',
        filename_output))
    
if __name__ == '__main__':
    sys.exit(main())
