import pyautogui
import pyperclip
import schedule
import time
import os

# --- 여기를 수정하세요 ---
# 1. 메시지를 보낼 카카오톡 대화방 이름
CHATROOM_NAME = "test방"

# 2. 보낼 메시지 목록 (시간과 메시지를 원하는 만큼 추가)
schedule_list = [
    {
        'time': '15:18', 
        'message': '첫 번째 예약 메시지입니다.'
    },
    {
        'time': '15:19', 
        'message': '두 번째 예약 메시지입니다.'
    }
]
# --------------------------

def send_kakaotalk_message(chatroom, message):
    """
    지정된 카카오톡 대화방에 메시지를 전송합니다.
    """
    try:
        print(f"카카오톡 메시지 전송 -> [{chatroom}] 방에 [{message}]")

        # 1. 카카오톡 앱 실행 또는 활성화
        os.system('open -a "KakaoTalk"')
        time.sleep(2)

        # 2. 대화방 이름으로 검색해서 들어가기
        pyautogui.hotkey('command', 'f')
        time.sleep(1)
        pyperclip.copy(chatroom)
        pyautogui.hotkey('command', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)

        # 3. 메시지 입력 및 전송
        pyperclip.copy(message)
        pyautogui.hotkey('command', 'v')
        time.sleep(1)
        pyautogui.press('enter')

        print(f"전송 완료: [{message}]")

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

def main():
    print("--- 카카오톡 메시지 예약 ---")
    print(f"대상 대화방: {CHATROOM_NAME}")
    
    if not schedule_list:
        print("예약된 메시지가 없습니다.")
        return

    # 각 스케줄을 등록
    for job in schedule_list:
        schedule_time = job.get('time')
        message_to_send = job.get('message')
        
        if not schedule_time or not message_to_send:
            continue
            
        schedule.every().day.at(schedule_time).do(send_kakaotalk_message, chatroom=CHATROOM_NAME, message=message_to_send)
        print(f"- 시간: {schedule_time}, 메시지: {message_to_send} (예약됨)")

    print("--------------------------")
    print("예약이 모두 설정되었습니다. 지정된 시간이 되면 메시지를 전송합니다.")
    print("이 창을 닫지 마세요. 스크립트가 실행 중이어야 합니다.")
    print("스크립트를 종료하려면 Ctrl + C 를 누르세요.")

    while True:
        # 한 번 실행된 작업은 리스트에서 제거하여 다음 날 다시 실행되지 않도록 함
        # 만약 매일 반복하고 싶다면 이 부분을 주석 처리하세요.
        jobs_to_remove = [j for j in schedule.jobs if not j.should_run]
        for j in jobs_to_remove:
            schedule.cancel_job(j)

        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    if os.name == 'posix':
        try:
            pyautogui.FAILSAFE = False
        except Exception:
            print("macOS 손쉬운 사용 권한을 확인해주세요.")

    main()