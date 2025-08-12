# https://www.fesliyanstudios.com/royalty-free-sound-effects-download/alarm-203
# https://dunsinoyekan.com/wp-content/uploads/2024/04/Dunsin-Oyekan_Worthy-Of-My-Praise_Alarm.mp3

# The code below is a simple alarm program. It uses the `playsound` library to play an audio file
# and the `time` library to create a countdown timer.
# The comments at the top are links to the sound files used, but they are not
# part of the Python code itself.

from playsound import playsound  # This line imports the function to play a sound file.
import time  # This line imports the time module, which allows us to work with time-related functions.

# ANSI escape codes are used to control the terminal's cursor and screen.
# They allow the program to clear the screen or move the cursor without
# printing a bunch of new lines.
CLEAR = "\033[2J"  # This code clears the entire terminal screen.
CLEAR_AND_RETURN = "\033[H"  # This code moves the cursor to the home position (top-left corner).


def alarm(seconds):
    """
    This function creates a countdown timer and plays an alarm sound when the time is up.

    Args:
        seconds (int): The total number of seconds for the alarm countdown.
    """
    time_elasped = 0  # Initialize a counter for the time that has passed.

    print(CLEAR)  # Clear the terminal screen before starting the countdown.
    while time_elasped < seconds:  # The loop continues until the elapsed time equals the total seconds.
        time.sleep(1)  # Pause the program for 1 second. This is the core of the countdown.
        time_elasped += 1  # Increment the elapsed time by 1 second.

        # Calculate the remaining time to display to the user.
        time_left = seconds - time_elasped
        minutes_left = time_left // 60  # Use integer division to get the number of full minutes.
        seconds_left = time_left % 60  # Use the modulo operator to get the remaining seconds.

        # Print the countdown.
        # The f-string formats the output. `CLEAR_AND_RETURN` moves the cursor
        # back to the top-left, so the new time overwrites the old one, creating
        # a smooth countdown effect. The `:02d` format specifier ensures that
        # minutes and seconds are always displayed with two digits (e.g., 05 instead of 5).
        print(f"{CLEAR_AND_RETURN}Alarm will sound in: {minutes_left:02d}:{seconds_left:02d}")

    # Once the loop finishes, the time is up. Play the alarm sound.
    # NOTE: You need to replace "FilePath/WakeUp.mp3" with the actual path to your sound file.
    playsound("FilePath/WakeUp.mp3")


# --- Main part of the script ---

# Prompt the user to enter the number of minutes and seconds for the alarm.
minutes = int(input("How many minutes to wait: "))
seconds = int(input("How many seconds to wait: "))
# Calculate the total number of seconds from the user's input.
total_seconds = minutes * 60 + seconds

# Call the `alarm` function with the total number of seconds.
alarm(total_seconds)
