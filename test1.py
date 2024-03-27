import pyautogui
from time import sleep

chrome_title = "Chrome"
activate_window_name = 'Google Translate - Google Chrome'
# Get the Chrome window and activate it using PyAutoGUI
# a = input('a = ')

chrome_windows = pyautogui.getWindowsWithTitle(chrome_title)
for window in chrome_windows:
    if str(window.title) == activate_window_name:
        window.activate()
