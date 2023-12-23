"""Script to automate deleting passwords from Google Chrome password manager."""
import time

from pynput.keyboard import Controller as CK
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput.mouse import Controller as CM

mouse = CM()
keyboard = CK()

dots = (1166.6875, 820.62109375)
remove = (1094.06640625, 891.35546875)
sleep = 0.3

with keyboard.pressed(Key.cmd):
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)

# Type 'Hello World' using the shortcut type method
keyboard.type("Hello World")

for i in range(5):
    mouse.position = dots
    time.sleep(sleep)
    mouse.click(Button.left, 1)

    mouse.position = remove
    time.sleep(sleep)
    mouse.click(Button.left, 1)
    time.sleep(sleep)
