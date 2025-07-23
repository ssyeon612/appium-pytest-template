import os
import glob
import requests
import sys
import json

# 유니코드 출력 처리 (Windows 환경 대응)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# 스크린샷 탐색
file_list = glob.glob("**/screenshots/failure_*.png", recursive=True)
if not file_list:
    print("❗ 실패 스크린샷 없음. 종료.")
    exit(0)

filepath = file_list[0]
print(f"📸 Uploading screenshot: {filepath}")

# 필수 환경변수 확인
slack_token = os.environ.get("SLACK_TOKEN")
slack_channel = os.environ.get("SLACK_CHANNEL")
webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

if not slack_token or not slack_channel:
    print("❗ SLACK_TOKEN 또는 SLACK_CHANNEL 환경변수가 없습니다.")
    exit(1)

# Slack 파일 업로드
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

try:
    json_res = res.json()
    if not json_res.get("ok"):
        print(f"❗ 파일 업로드 실패: {json_res}")
        exit(1)

    permalink = json_res.get("file", {}).get("permalink")
    if permalink and webhook_url:
        # Webhook으로 링크 전송 (미리보기 유도)
        payload = {"text": f"📷 실패 스크린샷 확인: {permalink}"}
        webhook_res = requests.post(
            webhook_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        print("📨 Webhook 전송 결과:", webhook_res.status_code)
    else:
        print("⚠️ permalink 또는 SLACK_WEBHOOK_URL 누락 - 미리보기 생략됨")

except Exception as e:
    print("❗ Slack 응답 파싱 실패:", e)
    print("응답 상태코드:", res.status_code)
    print("응답 본문:", res.text)
