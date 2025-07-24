import pytest, time, os, requests, json, sys, glob
from datetime import datetime
from utils.driver_factory import create_driver

# === 옵션 추가 ===
def pytest_addoption(parser):
    parser.addoption(
        "--platform", action="store", default="android", help="Platform to test on: android or ios"
    )

# === 드라이버 설정 ===
@pytest.fixture(scope="function")
def driver(request):
    platform = request.config.getoption("--platform")
    try:
        driver = create_driver(platform)
    except Exception as e:
        print("Driver 생성 실패:", e)
        raise
    yield driver

    # 실패 시 스크린샷 저장
    if request.node.rep_call.failed:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        folder = "screenshots"
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, f"failure_{timestamp}.png")
        driver.save_screenshot(filename)
        print(f"[SCREENSHOT] 테스트 실패 - 스크린샷 저장됨: {filename}")

    driver.quit()

# === hook: 테스트 결과를 fixture에서 알 수 있게 해주는 코드 ===
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     rep = outcome.get_result()
#     setattr(item, "rep_" + rep.when, rep)

# # Windows UTF-8 출력 설정
# try:
#     sys.stdout.reconfigure(encoding='utf-8')
# except Exception:
#     pass

# # === 테스트 종료 후 Slack 메시지 전송 ===
# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     passed = len(terminalreporter.stats.get('passed', []))
#     failed = len(terminalreporter.stats.get('failed', []))
#     skipped = len(terminalreporter.stats.get('skipped', []))

#     slack_token = os.environ.get("SLACK_TOKEN")
#     slack_channel = os.environ.get("SLACK_CHANNEL")

#     if not slack_token or not slack_channel:
#         print("❗ SLACK_TOKEN 또는 SLACK_CHANNEL 환경변수가 설정되어 있지 않습니다.")
#         return

#     # === 1. 테스트 결과 메시지 전송 ===
#     emoji = "✅ 성공" if failed == 0 else "❌ 실패"
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     message = {
#         "channel": slack_channel,
#         "text": (
#             f"{emoji}: 로컬 테스트 완료\n"
#             f"📊 테스트 결과: {passed} passed / {failed} failed / {skipped} skipped\n"
#             f"🕒 실행 시간: {timestamp}"
#         )
#     }

#     try:
#         res = requests.post(
#             "https://slack.com/api/chat.postMessage",
#             headers={
#                 "Authorization": f"Bearer {slack_token}",
#                 "Content-Type": "application/json"
#             },
#             data=json.dumps(message)
#         )
#         print("📨 Slack 메시지 전송 결과:", res.json())
#     except Exception as e:
#         print("❌ Slack 메시지 전송 실패:", e)

#     # === 2. 실패 시 스크린샷 업로드 ===
#     if failed > 0:
#         file_list = glob.glob("**/screenshots/failure_*.png", recursive=True)
#         if not file_list:
#             print("❗ 스크린샷 없음")
#             return
        
#         # 오래된 스크린샷 자동 정리 (최신 5개만 유지)
#         file_list.sort(key=os.path.getmtime, reverse=True)  # 최신 순 정렬
#         max_keep = 5 
#         for old_file in file_list[max_keep:]:
#             try:
#                 os.remove(old_file)
#                 print(f"🧹 오래된 스크린샷 삭제됨: {old_file}")
#             except Exception as e:
#                 print(f"⚠️ 삭제 실패: {old_file} - {e}")
        
#         # 최신 스크린샷 선택
#         filepath = file_list[0]
#         filename = os.path.basename(filepath)
#         file_size = int(os.path.getsize(filepath))
#         print(f"📸 Uploading screenshot: {filepath}")

#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {slack_token}'
#         }
#         # Step 1: 업로드 URL 요청
#         data  = {
#             "filename": filename,
#             "length": file_size
#         }
#         headers['Content-Type'] = 'application/x-www-form-urlencoded'
#         res = requests.post(
#             "https://slack.com/api/files.getUploadURLExternal",
#             headers=headers,
#             data=data 
#         )

#         try:
#             res_json = res.json()
#         except Exception:
#             print("❗ 응답 파싱 실패:", res.text)
#             return

#         if not res_json.get("ok"):
#             print("❗ upload URL 요청 실패:", res_json)
#             return

#         upload_url = res_json["upload_url"]
#         file_id = res_json["file_id"]

#         print(f'upload_url - {upload_url} / file_id - {file_id}')

#         # Step 2: upload image
#         with open(filepath, "rb") as f:
#             put_res = requests.post(upload_url, data=f)
#         if put_res.status_code != 200:
#             print("❗ 파일 업로드 실패 (PUT):", put_res.status_code, put_res.text)
#             return

#         # Step 3: 공유 완료
#         attachment = {
#             "files": [{
#                     "id": file_id,
#                     "title": f"테스트 실패 스크린샷 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
#                 }],
#             "channel_id": slack_channel,
#         }
#         headers['Content-Type'] = 'application/json; charset=utf-8'
#         complete_res = requests.post(
#             url="https://slack.com/api/files.completeUploadExternal",
#             headers=headers,
#             json=attachment
#         )

#         comp_json = complete_res.json()
#         if comp_json.get("ok"):
#             print("✅ 스크린샷 업로드 성공!")
#         else:
#             print("❗ 완료 단계 실패:", comp_json)
