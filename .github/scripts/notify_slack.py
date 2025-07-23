import os
import glob
import requests
import sys
import json

# Windows 인코딩 문제 방지
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# 스크린샷 파일 탐색
file_list = glob.glob("**/screenshots/failure_*.png", recursive=True)
if not file_list:
    print("❗ 실패 스크린샷 없음. 종료.")
    exit(0)

filepath = file_list[0]
print(f"📸 Uploading screenshot: {filepath}")

# Slack 인증 정보
token = os.environ.get("SLACK_TOKEN")
channel = os.environ.get("SLACK_CHANNEL")

if not token or not channel:
    print("❗ SLACK_TOKEN 또는 SLACK_CHANNEL 환경변수가 없습니다.")
    exit(1)

# 1차 업로드: 파일 업로드 API
with open(filepath, "rb") as f:
    res = requests.post(
        url="https://slack.com/api/files.upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": f},
        data={
            "channels": channel,
            "filename": os.path.basename(filepath),
            "initial_comment": "❌ 테스트 실패 - 실행 스크린샷 첨부"
        }
    )

# 응답 처리
if not res.ok or not res.json().get("ok"):
    print("❗ 파일 업로드 실패:", res.text)
    exit(1)

file_info = res.json().get("file", {})
permalink = file_info.get("permalink")

if permalink:
    print("📎 Slack 이미지 링크:", permalink)

    # 2차 전송: Webhook으로 링크 전송 (미리보기 유도)
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if webhook_url:
        payload = {
            "text": f"📷 실패 스크린샷 확인: {permalink}"
        }
        hook_res = requests.post(
            webhook_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        print("📨 Webhook 전송 결과:", hook_res.status_code)
    else:
        print("⚠️ SLACK_WEBHOOK_URL 이 설정되어 있지 않아 이미지 링크 전송은 생략됩니다.")
else:
    print("⚠️ permalink 정보가 없습니다.")
