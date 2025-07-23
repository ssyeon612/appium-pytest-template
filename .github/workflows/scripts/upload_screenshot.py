import os
import glob
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")

file_list = glob.glob("**/screenshots/failure_*.png", recursive=True)
if not file_list:
    print("❗ No screenshot found")
    exit(0)

filepath = file_list[0]
print(f"📸 Uploading screenshot: {filepath}")

with open(filepath, "rb") as f:
    res = requests.post(
        url="https://slack.com/api/files.upload",
        headers={"Authorization": f"Bearer {SLACK_TOKEN}"},
        files={"file": f},
        data={
            "channels": SLACK_CHANNEL,
            "initial_comment": "❌ 테스트 실패 - 실행 스크린샷 첨부",
            "filename": os.path.basename(filepath),
        },
    )
    print(res.json())
