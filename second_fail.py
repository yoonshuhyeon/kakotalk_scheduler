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
    pyautogui.press('enter')
    print(f"\n{time.strftime('%H:%M:%S')} - 메시지 전송 완료 (Enter).")


def prepare_messages(messages_to_prepare, delay_seconds=2):
    """
    카카오톡 대화방에 메시지를 미리 입력해둡니다.
    """
    try:
        # 1. 카카오톡 앱 실행 또는 활성화
        os.system('open -a "KakaoTalk"')
        time.sleep(2)

        # 2. 대화방 이름으로 검색해서 들어가기
        pyautogui.hotkey('command', 'f')
        time.sleep(1)
        pypercip.copy(CHATROOM_NAME)
        pyautogui.hotkey('command', 'v')
        time.sleep(3)
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(2)

        # 3. (추가됨) 메시지 입력창을 찾아서 클릭하여 커서를 활성화합니다.
        try:
            input_location = pyautogui.locateCenterOnScreen('kakaotalk_input.png', confidence=0.8)
        except pyautogui.ImageNotFoundException:
            input_location = None
        if input_location is None:
            print("\n경고: 메시지 입력창('kakaotalk_input.png')을 찾지 못했습니다. 메시지 전송을 그냥 시도합니다.")
            time.sleep(1)
        else:
            pyautogui.click(input_location)
            time.sleep(1)

        # 4. 메시지 준비
        print(f"\n{time.strftime('%H:%M:%S')} - 메시지 전송을 준비합니다...")
        
        # 여러 개의 메시지 중 마지막 메시지를 제외하고 모두 전송
        for i in range(len(messages_to_prepare) - 1):
            message = messages_to_prepare[i]
            print(f"사전 전송 중: {message}")
            pyperclip.copy(message)
            pyautogui.hotkey('command', 'v')
            pyautogui.press('enter')
            time.sleep(delay_seconds)

        # 마지막 메시지는 입력만 하고 Enter는 누르지 않음
        if messages_to_prepare:
            last_message = messages_to_prepare[-1]
            print(f"전송 대기 메시지 입력: {last_message}")
            pyperclip.copy(last_message)
            pyautogui.hotkey('command', 'v')
        
        print("메시지 입력 완료. 전송 시간을 기다립니다.")

    except Exception as e:
        error_message = f"오류 발생 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        error_message += f"오류 타입: {type(e).__name__}\n"
        error_message += f"오류 메시지: {e}\n"
        error_message += f"Traceback:\n{traceback.format_exc()}\n"
        print(f"\n오류가 발생했습니다. 자세한 내용은 error_log.txt 파일을 확인해주세요.")
        with open("error_log.txt", "a", encoding="utf-8") as f:
            f.write(error_message + "-"*20 + "\n")

# --- 대화방 설정 ---
CHATROOM_NAME = "눈 동그랗게 떠 송하영🍀"
# --------------------

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
        print(f"NTP 서버 연결 실패: {e}")
        print("시간 오차 보정 없이 로컬 시간으로 진행합니다.")
        return 0

def main():
    # --- 여기를 수정하세요 ---
    schedule_list = [
        {
            'time': '01:11:00', 
            'messages': [
                '111'
            ]
        },
        {
            'time': '02:22:00', 
            'messages': [
                '222'
            ]
        },
        {
            'time': '03:33:00', 
            'messages': [
                '333'
            ]
        },
        {
            'time': '05:55:00', 
            'messages': [
                '555'
            ]
        },
        {
            'time': '11:11:00', 
            'messages': [
                '1111'
            ]
        },
        {
            'time': '13:11:00', 
            'messages': [
                '111'
            ]
        },
        {
            'time': '14:22:00', 
            'messages': [
                '222'
            ]
        },
        {
            'time': '15:33:00', 
            'messages': [
                '333'
            ]
        },
        {
            'time': '17:55:00', 
            'messages': [
                '555'
            ]
        },
        {
            'time': '23:11:00', 
            'messages': [
                '1111'
            ]
        },
        {
            'time': '21:00:00', 
            'messages': [
                '빵속시'
            ]
        },
        {
            'time': '09:29:00', 
            'messages': [
                '빵시'
            ]
        },
        {
            'time': '21:00:00', 
            'messages': [
                '빵속시'
            ]
        },
        {
            'time': '21:29:00', 
            'messages': [
                '빵시'
            ]
        }
    ]
    # --------------------------

    offset = get_time_offset()

    print("--- 스케줄 목록 ---")
    for job in schedule_list:
        h, m, s = map(int, job['time'].split(':'))
        job_time_today = datetime.now().replace(hour=h, minute=m, second=s, microsecond=0)
        
        # 최종 전송 시간 계산
        final_send_time = job_time_today + timedelta(seconds=offset)
        final_send_time_schedule_str = final_send_time.strftime("%H:%M:%S")
        final_send_time_display_str = final_send_time.strftime("%H:%M:%S.%f")[:-3]

        # 준비 시간 계산 (전송 15초 전)
        prep_time = final_send_time - timedelta(seconds=15)
        prep_time_schedule_str = prep_time.strftime("%H:%M:%S")
        prep_time_display_str = prep_time.strftime("%H:%M:%S.%f")[:-3]

        # 스케줄 등록
        schedule.every().day.at(prep_time_schedule_str).do(prepare_messages, messages_to_prepare=job['messages'])
        schedule.every().day.at(final_send_time_schedule_str).do(commit_last_message)
        
        print(f"- {job['time']} 전송 예약됨 (준비: {prep_time_display_str}, 전송: {final_send_time_display_str}) | 메시지 {len(job['messages'])}개")
    
    print("-------------------")
    print("스크립트가 시작되었습니다. 스케줄에 따라 메시지를 전송합니다.")
    print("스크립트를 종료하려면 Ctrl + C 를 누르세요.")

    while True:
        schedule.run_pending()
        corrected_now = datetime.now() - timedelta(seconds=offset)
        corrected_now_str = corrected_now.strftime("%H:%M:%S")
        print(f"현재 시각(보정됨): {corrected_now_str} | 다음 전송 대기 중...           ", end="\r")
        time.sleep(1)

if __name__ == "__main__":
    if sys.platform == 'darwin':
        try:
            pyautogui.FAILSAFE = False
        except Exception:
            print("macOS 손쉬운 사용 권한이 필요할 수 있습니다.")

    main()
