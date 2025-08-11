# https://www.fesliyanstudios.com/royalty-free-sound-effects-download/alarm-203
# https://dunsinoyekan.com/wp-content/uploads/2024/04/Dunsin-Oyekan_Worthy-Of-My-Praise_Alarm.mp3
from playsound import playsound
import time

#ANSI
CLEAR = "\033[2J"
CLEAR_AND_RETURN = "\033[H"

def alarm(seconds):
    time_elasped = 0

    print(CLEAR)
    while time_elasped < seconds:
        time.sleep(1)
        time_elasped += 1

        time_left = seconds - time_elasped
        minutes_left = time_left // 60
        seconds_left = time_left % 60

        print(f"{CLEAR_AND_RETURN}Alarm will sound in: {minutes_left:02d}:{seconds_left:02d}")

    playsound("FilePath/WakeUp.mp3")

minutes = int(input("How many minutes to wait: "))
seconds = int(input("How many seconds to wait: "))
total_seconds = minutes * 60 + seconds

alarm(total_seconds)
