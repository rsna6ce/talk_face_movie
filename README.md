# talk_face_movie

https://github.com/rsna6ce/talk_face_movie/assets/86136223/1d628e52-5d59-4937-961b-8db66fa95ff0

## Overview
* The talk_face_movie is a tool that creates a video of a talking face according to the audio of the input wav file.
* input:wav file and 4 face files.
* output:mp4 file

## Setup environment
install python environment
```
$ cd talk_face_movie
$ sudo apt install python3-pip
$ pip3 install -r requirements.txt
```

install ffmpeg environment
```
$ sudo apt install ffmpeg
```

## How to use
* setup face picture
    * 4 Images must have the same width and height
    * picture/face_1.png : close mouth with open eyes
    * picture/face_2.png : open mouth small with open eyes
    * picture/face_3.png : open mouth large with open eyes
    * picture/face_4.png : close mouth with close eyes

* help
```
$ ./talk_face_movie.py -h
usage: talk_face_movie.py [-h] -i INPUT -o OUTPUT [-f FRAME_RATE] [-p PICTURE_DIR] [-s SMALL_THRESHOLD] [-l LARGE_THRESHOLD] [-b BLINK_INTERVAL]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input wav file
  -o OUTPUT, --output OUTPUT
                        output mp4 file
  -f FRAME_RATE, --frame_rate FRAME_RATE
                        frame_rate fps
  -p PICTURE_DIR, --picture_dir PICTURE_DIR
                        directory of face picture
  -s SMALL_THRESHOLD, --small_threshold SMALL_THRESHOLD
                        small mouth sound threshold
  -l LARGE_THRESHOLD, --large_threshold LARGE_THRESHOLD
                        large mouth sound threshold
  -b BLINK_INTERVAL, --blink_interval BLINK_INTERVAL
                        blink interval (ms)
```

* run (sample)
```
$ python3 talk_face_movie.py -i sample.wav -o sample.mp4
```

*clean up
```
$ cd talk_face_movie
$ rm temp/*.png
& rm temp.mp4
```
