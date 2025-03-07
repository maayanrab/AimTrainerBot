from typing import Literal
from pyautogui import *
import pyautogui
import random
import keyboard
import win32api
import win32con
import webbrowser
from file_names import *
import game_modes
import keyboard_keys
import urls

CHECK_GAMEOVER = True


def is_image_on_screen(img_filename, grayscale=False, region=None, confidence=0.8):
    try:
        img = pyautogui.locateOnScreen(
            img_filename,
            grayscale=grayscale,
            confidence=confidence,
            region=region  # tuple: (startXValue, startYValue, width, height)
        )
        center_point = pyautogui.center(img)  # image found
        return center_point
    except:  # image not found
        return None


# command to get screen area and colors
# pyautogui.displayMousePosition()

target_color = (255, 87, 34)
screen_region = (674, 484, 1872-674, 1206-484)


def click(x: int, y: int):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def autoplay(game_mode: Literal["challenge", "precision"], target_filename=None):

    while not keyboard.is_pressed(keyboard_keys.stop_key):

        if CHECK_GAMEOVER and is_image_on_screen(play_file, grayscale=True, region=screen_region) is not None:
            print("GAME OVER")
            exit(1)

        if game_mode == game_modes.challenge:

            target_acquired = 0
            pic = pyautogui.screenshot(region=screen_region)
            width, height = pic.size

            for x in range(0, width, 5):
                for y in range(0, height, 5):
                    r, g, b = pic.getpixel((x, y))

                    if b == target_color[2] and r == target_color[0] and g == target_color[1]:
                        target_acquired = 1
                        click(x + screen_region[0], y + screen_region[1])
                        sleep(random.uniform(0.02, 0.07))  # sleep random time between 0.02 and 0.07 to pass detector
                        break

                if target_acquired == 1:
                    break

        elif game_mode == game_modes.precision:
            center_point = is_image_on_screen(target_filename, region=screen_region, confidence=0.6)

            if center_point is not None:
                print("Target acquired!")
                click(center_point[0], center_point[1])
                sleep(random.uniform(0.02, 0.07))  # sleep random time between 0.02 and 0.07 to pass detector
            else:
                print("Target not found.")

    quit_game_by_q()


def autoplay_precision():
    autoplay(game_mode=game_modes.precision,
             target_filename=precision_target_file)


def autoplay_challenge():
    autoplay(game_mode=game_modes.challenge)


def quit_game_by_q():
    exit(f"Program was terminated by {keyboard_keys.stop_key.capitalize()} press")


play = {
    game_modes.precision: autoplay_precision,
    game_modes.challenge: autoplay_challenge
}

url = {
    game_modes.precision: urls.precision_url,
    game_modes.challenge: urls.challenge_url
}

#   ##########################################       CHOOSE GAME MODE:       ##########################################
mode = game_modes.challenge


print(f"{mode.capitalize()} mode was chosen.")
print("Hold Q to stop autoclicker.")
wait_time = 3
print("Starting in...")
for i in range(wait_time)[::-1]:
    print(i + 1)
    sleep(1)
webbrowser.open(url[mode])

play_point = None
while not play_point:
    play_point = is_image_on_screen(play_file, region=screen_region)

if mode == game_modes.precision:
    hard_point = None
    while not hard_point:
        hard_point = is_image_on_screen(hard_setting_file, region=screen_region)
    click(hard_point[0], hard_point[1])
    sleep(0.5)

click(play_point[0], play_point[1])
print("Game started!")
play[mode]()
