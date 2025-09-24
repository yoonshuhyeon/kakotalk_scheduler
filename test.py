import pyautogui
import pyperclip
import schedule
import time
import sys
import traceback
import os
import ntplib
from datetime import datetime, timedelta

def commit_last_message():
    """
    미리 입력된 메시지를 전송하기 위해 Enter 키를 누릅니다.
    """
    try:
        pyautogui.press('enter')
        print(f"\n{time.strftime('%H:%M:%S')} - 메시지 전송 완료 (Enter).")
    except Exception as e:
        print(f"Enter 전송 중 오류 발생: {e}")

def prepare_messages(chatroom_name, messages_to_prepare, delay_seconds=1):
    """
    카카오톡 대화방에 메시지를 미리 입력해둡니다.
    """
    try:
        # 1. 카카오톡 앱 활성화 및 검색창 열기
        print(f"\n{time.strftime('%H:%M:%S')} - 메시지 준비를 시작합니다...")
        os.system("osascript -e 'tell application \"KakaoTalk\" to activate' -e 'delay 1' -e 'tell application \"System Events\" to keystroke \"f\" using command down'")
        time.sleep(1)

        # 2. 대화방 이름으로 검색해서 들어가기
        pyperclip.copy(chatroom_name)
        pyautogui.hotkey('command', 'v')
        time.sleep(2)
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(2)

        # 3. 메시지 입력창 찾아서 클릭 (이미지 기반, 실패해도 계속 진행)
        try:
            input_location = pyautogui.locateCenterOnScreen('kakaotalk_input.png', confidence=0.8)
            if input_location:
                pyautogui.click(input_location)
                time.sleep(0.5)
        except pyautogui.ImageNotFoundException:
            pass # 이미지를 못찾아도 그냥 진행

        # 4. 메시지 준비
        print(f"'{chatroom_name}' 방에 메시지를 준비합니다.")
        
        # 마지막 메시지를 제외하고 모두 전송
        for i in range(len(messages_to_prepare) - 1):
            message = messages_to_prepare[i]
            pyperclip.copy(message)
            os.system("osascript -e 'tell application \"System Events\" to keystroke \"v\" using command down'")
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(delay_seconds)
            print(f"  - 사전 전송: {message}")

        # 마지막 메시지는 입력만 하고 Enter는 누르지 않음
        if messages_to_prepare:
            last_message = messages_to_prepare[-1]
            pyperclip.copy(last_message)
            os.system("osascript -e 'tell application \"System Events\" to keystroke \"v\" using command down'")
            print(f"  - 전송 대기: {last_message}")
        
        print("메시지 입력 완료. 전송 시간을 기다립니다.")

    except Exception as e:
        error_message = f"오류 발생 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        error_message += f"오류 타입: {type(e).__name__}\n"
        error_message += f"오류 메시지: {e}\n"
        error_message += f"Traceback:\n{traceback.format_exc()}\n"
        print(f"\n오류가 발생했습니다. 자세한 내용은 error_log.txt 파일을 확인해주세요.")
        with open("error_log.txt", "a", encoding="utf-8") as f:
            f.write(error_message + "-"*20 + "\n")

def get_time_offset():
    """
    NTP 서버와 로컬 시간의 오차를 초 단위로 반환합니다.
    """
    try:
        client = ntplib.NTPClient()
        response = client.request('time.google.com', version=3)
        offset = response.offset
        print(f"시간 오차 보정: {offset:.4f}초")
        return offset
    except Exception as e:
        print(f"NTP 서버 연결 실패: {e}. 시간 오차 보정 없이 로컬 시간으로 진행합니다.")
        return 0

def main():
    # --- 여기를 수정하세요 ---
    CHATROOM_NAME = "test방"
    PREP_SECONDS = 15 # 몇 초 전에 준비를 시작할지
    schedule_list = [
        {
            'time': '01:11:00', 
            'messages': ['111']
        },
        {
            'time': '15:30:00', 
            'messages': ['두 번째 예약 메시지입니다.']
        }
    ]
    # --------------------------

    offset = get_time_offset()

    print("--- 스케줄 목록 ---")
    for job in schedule_list:
        h, m, s = map(int, job['time'].split(':'))
        job_time_today = datetime.now().replace(hour=h, minute=m, second=s, microsecond=0)
        
        # 최종 전송 시간 (오차 보정)
        final_send_time = job_time_today - timedelta(seconds=offset)
        final_send_time_schedule_str = final_send_time.strftime("%H:%M:%S")

        # 준비 시간
        prep_time = final_send_time - timedelta(seconds=PREP_SECONDS)
        prep_time_schedule_str = prep_time.strftime("%H:%M:%S")

        # 스케줄 등록
        schedule.every().day.at(prep_time_schedule_str).do(prepare_messages, chatroom_name=CHATROOM_NAME, messages_to_prepare=job['messages'])
        schedule.every().day.at(final_send_time_schedule_str).do(commit_last_message)
        
        print(f"- {job['time']} 예약 (준비: {prep_time.strftime('%T')}, 전송: {final_send_time.strftime('%T')})")
    
    print("-------------------")
    print("스크립트가 시작되었습니다. 스케줄에 따라 메시지를 전송합니다.")

    while True:
        schedule.run_pending()
        # 보정된 현재 시간 표시 (사용자 편의성)
        corrected_now = datetime.now() + timedelta(seconds=offset)
        print(f"현재 시각(보정됨): {corrected_now.strftime('%H:%M:%S')} | 다음 전송 대기 중...", end="\r")
        time.sleep(1)

if __name__ == "__main__":
    if sys.platform == 'darwin':
        try:
            pyautogui.FAILSAFE = False
        except Exception:
            print("macOS 손쉬운 사용 권한이 필요할 수 있습니다.")
            print("시스템 설정 > 개인정보 보호 및 보안 > 손쉬운 사용 > 터미널 또는 사용하는 앱을 추가해주세요.")

    main()