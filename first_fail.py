import pyautogui
import pyperclip
import time

kakaotalk = "카카오톡"
roomname = 'test방'
t=0

pyautogui.keyDown('command')
pyautogui.press('space')
pyautogui.keyUp('command')
pyperclip.copy(kakaotalk)
pyautogui.keyDown('command')
pyautogui.press('v')
pyautogui.keyUp('command')
pyautogui.press('enter')
pyautogui.keyDown('command')
pyautogui.press('f')
pyautogui.keyUp('command')
pyperclip.copy(roomname)
pyautogui.keyDown('command')
pyautogui.press('v')
pyautogui.keyUp('command')
pyautogui.press('enter')
time.sleep(1)
pyautogui.press('down')
pyautogui.press('enter')
time.sleep(1)
print(f'1초 기달림')
pyautogui.press('capslock')
pyautogui.hotkey('a')

