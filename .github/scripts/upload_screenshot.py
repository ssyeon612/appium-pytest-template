import os
import glob
import requests
import sys
import json

# 출력 인코딩 설정 (Windows PowerShell 대응)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# 실패 스크린샷 탐색
file_list = glob.glob("**/screenshots/failure_*.png", recursive=True)
if not file_list:
    print("❗ 실패 스크린샷 없음. 종료.")
    exit(0)

filepath = file_list[0]
print(f"📸 Uploading screenshot: {filepath}")

# 환경변수 로딩
slack_token = os.environ.get("SLACK_TOKEN")
slack_channel = os.environ.get("SLACK_CHANNEL")

if not slack_token or not slack_channel:
    print("❗ SLACK_TOKEN 또는 SLACK_CHANNEL 환경변수가 없습니다.")
    exit(1)

# 파일 업로드
with open(filepath, "rb") as f:
    res = requests.post(
        url="https://slack.com/api/files.upload",
        headers={"Authorization": f"Bearer {slack_token}"},
        files={"file": f},
        data={
            "channels": slack_channel,
            "filename": os.path.basename(filepath),
            "initial_comment": "❌ 테스트 실패 - 실행 스크린샷 첨부"
        }
    )

upload_result = res.json()
if not res.ok or not upload_result.get("ok"):
    print("❗ 파일 업로드 실패:", upload_result)
    exit(1)

# 업로드된 파일의 permalink 추출
file_info = upload_result.get("file", {})
permalink = file_info.get("permalink")
if not permalink:
    print("⚠️ permalink 정보 없음.")
    exit(1)

# 이미지 표시 메시지 전송
message_payload = {
    "channel": slack_channel,
    "text": "❌ 테스트 실패 스크린샷",
    "blocks": [
        {
            "type": "image",
            "image_url": permalink,
            "alt_text": "테스트 실패 스크린샷"
        }
    ]
}

msg_res = requests.post(
    "https://slack.com/api/chat.postMessage",
    headers={
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    },
    data=json.dumps(message_payload)
)

try:
    print("📨 Slack 메시지 전송 응답:", msg_res.json())
except Exception as e:
    print("⚠️ 메시지 응답 파싱 실패:", e)
    print("응답 상태코드:", msg_res.status_code)
    print("응답 본문:", msg_res.text)
