import pyautogui
import time

print("좌표 찾기를 시작합니다. 원하는 위치에 마우스를 올리고 Ctrl+C를 누르세요.")
print("Press Ctrl-C to quit.")

try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print('\n좌표 찾기를 종료합니다.')
