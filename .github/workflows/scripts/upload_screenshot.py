import os
import glob
import requests

file_list = glob.glob("**/screenshots/failure_*.png", recursive=True)
if not file_list:
    print("❗ No screenshot found")
    exit(0)

filepath = file_list[0]
print(f"Uploading screenshot: {filepath}")

with open(filepath, "rb") as f:
    res = requests.post(
        url="https://slack.com/api/files.upload",
        headers={"Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"},
        files={"file": f},
        data={
            "channels": os.environ["SLACK_CHANNEL"],
            "initial_comment": "❌ 테스트 실패 - 실행 스크린샷 첨부",
            "filename": os.path.basename(filepath),
        },
    )
    print(res.json())
