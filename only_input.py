import pyautogui
import pyperclip
import schedule
import time
from datetime import datetime, timedelta
import os
import pytz
import re

# --- 시간 보정 설정 ---
time_offset = timedelta(0)
KST = pytz.timezone('Asia/Seoul')

def calibrate_time():
    """
    Google 서버 시간을 가져와 로컬 시스템 시간과의 차이를 계산하여 보정합니다.
    """
    global time_offset
    try:
        # curl 명령을 실행하여 google.com의 헤더를 가져옵니다.
        with os.popen('curl -Is https://www.google.com') as stream:
            headers = stream.read()
        
        # Date 헤더를 찾습니다.
        date_header = re.search(r"^Date: (.*)$", headers, re.MULTILINE | re.IGNORECASE)
        if not date_header:
            raise ValueError("Google 응답에서 Date 헤더를 찾을 수 없습니다.")

        date_str = date_header.group(1).strip()
        # 헤더의 GMT 시간을 파싱합니다.
        google_time_gmt = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        # 파싱된 시간은 naive하지만 GMT입니다. 이를 UTC로 취급합니다.
        google_time_utc = google_time_gmt.replace(tzinfo=pytz.utc)

        # 현재 시스템 시간을 timezone-aware UTC로 가져옵니다.
        system_time_utc = datetime.now(pytz.utc)

        # 시간 차이를 계산합니다.
        time_offset = google_time_utc - system_time_utc
        
        print(f"✅ 시간 보정 완료. Google 서버와의 시간 차이: {time_offset}")

    except Exception as e:
        print(f"⚠️ Google 시간 동기화 실패: {e}. 시스템 시간을 사용합니다.")
        time_offset = timedelta(0)

def get_corrected_kst_time():
    """
    Google 서버 시간으로 보정된 현재 한국 시간을 반환합니다.
    """
    # 현재 시스템 시간을 timezone-aware UTC로 가져와 시간 차이를 적용합니다.
    corrected_utc_time = datetime.now(pytz.utc) + time_offset
    # KST로 변환합니다.
    return corrected_utc_time.astimezone(KST)
# ------------------------


# --- 여기에 원하는 시간과 메시지를 설정하세요. ---
schedule_list = [
    {
        'time': '09:00:00',
        'messages': '굿모닝'
    },
    {
        'time': '12:00',
        'messages': '점심 먹을 시간'
    }
]
# ------------------------------------------------

def clear_screen():
    """콘솔 화면을 지웁니다."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_next_job_string():
    """
    schedule_list를 기반으로 다음 실행될 작업 정보를 찾아 문자열로 반환합니다.
    """
    now = get_corrected_kst_time().time()
    next_job = None
    
    # 이 함수가 호출되기 전에 schedule_list가 정렬되었다고 가정합니다.
    for job in schedule_list:
        if datetime.strptime(job['time'], '%H:%M:%S').time() > now:
            next_job = job
            break
    
    if next_job is None and schedule_list:
        next_job = schedule_list[0]

    if next_job:
        return f"🕒 다음 실행 예정: {next_job['time']} - '{next_job['messages']}'"
    else:
        return "실행할 스케줄이 없습니다."

def paste_message(message):
    """
    지정된 메시지를 클립보드에 복사한 후, 현재 활성화된 창에 붙여넣고 Enter를 누릅니다.
    """
    clear_screen()
    print(f"
[{get_corrected_kst_time().strftime('%Y-%m-%d %H:%M:%S')}] 실행: '{message}' 메시지를 붙여넣고 전송합니다.")
    pyperclip.copy(message)
    
    pyautogui.keyDown('command')
    pyautogui.press('v')
    pyautogui.keyUp('command')
    
    time.sleep(0.1)
    pyautogui.press('enter')
    
    # 메인 루프가 화면 업데이트를 처리하므로 1초간 메시지를 보여주기 위해 대기합니다.
    time.sleep(1)

def main():
    # 시간 보정 실행
    calibrate_time()

    # 초기 설정
    for job in schedule_list:
        schedule.every().day.at(job['time']).do(paste_message, message=job['messages'])

    # 시간순으로 스케줄 정렬
    schedule_list.sort(key=lambda x: datetime.strptime(x['time'], '%H:%M:%S').time())
    
    while True:
        clear_screen()
        
        print("✅ 스케줄러가 실행 중입니다. (종료: Ctrl+C)")
        print("-" * 40)

        # 전체 스케줄 목록 출력
        print("--- 예약된 모든 스케줄 ---")
        for job in schedule_list:
            print(f"  - {job['time']}: '{job['messages']}'")
        print("-" * 40)

        # 다음 스케줄 및 현재 시간 출력
        next_job_str = get_next_job_string()
        print(next_job_str)
        print(f"⏰ 현재 시간: {get_corrected_kst_time().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 40)

        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("
프로그램을 종료합니다.")

# Modified to allow git push
