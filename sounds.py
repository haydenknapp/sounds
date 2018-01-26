import glob, os
from pygame import mixer
import time
from mutagen.mp3 import MP3
import RPi.GPIO as GPIO
import random

pressed = False

def pressedCallback(dummy):
    print("Received press")
    global pressed
    pressed = True
    time.sleep(0.1)

def getmp3FileNames():
    ret = []
    os.chdir('/home/pi/Music/MP3Collection/')
    for file in glob.glob("*.mp3"):
        ret.append(file)
    return ret

if __name__ == '__main__':
    # initialize the random seed
    random.seed(time.time())

    # global pressed variable
    global pressed

    # prepare the gpio
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.IN)
    GPIO.add_event_detect(2, GPIO.FALLING)
    GPIO.add_event_callback(2, pressedCallback)

    # the minimum time in seconds for each coin insertion
    minTime = 15

    # get all of the filenames from the current directory
    filenames = getmp3FileNames()

    # initialize the mixer
    mixer.init() 

    # continuous loop
    while (True):
        # wait for the button to become pressed
        while pressed == False:
            time.sleep(0.5)
            print("waiting")

        time.sleep(0.3)
        pressed = False

        # the start time of the clip
        audioStartTime = time.time()

        # continue to play sounds until the elapsed time is greater
        while (time.time() - audioStartTime) < minTime:
            print(time.time() - audioStartTime)
            print(minTime)
            # select a random clip to play
            soundIndex = int(random.random() * len(filenames))

            # get the length of the audio clip
            clipLength = MP3(filenames[soundIndex]).info.length

            # play and load the audio clip
            mixer.music.load(filenames[soundIndex])
            mixer.music.play()
            print("Playing a new clip now: ", filenames[soundIndex])
            audioStartTimeIndi = time.time()

            # sleep for the length of the clip
            # time.sleep(clipLength)
            while time.time() - audioStartTimeIndi < clipLength:
                time.sleep(0.1)

            if pressed == True:
                audioStartTime = time.time()
                pressed = False


