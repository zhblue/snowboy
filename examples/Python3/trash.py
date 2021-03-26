import snowboydecoder
import sys
import os
import signal

# Demo code for listening to two hotwords at the same time

interrupted = False
def openKitchen():
    print("Kitchen")
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
    os.system("lcd 4 5 Kitchen")

def openOther():
    print("Other")
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    os.system("lcd 4 5 Other")

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) != 3:
    print("Error: need to specify 2 model names")
    print("Usage: python demo.py 1st.model 2nd.model")
    sys.exit(-1)

models = sys.argv[1:]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [lambda: openKitchen(),
             lambda: openOther()]
print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
