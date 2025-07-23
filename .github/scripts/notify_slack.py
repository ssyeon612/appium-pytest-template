import os
import json
import requests
from datetime import datetime

status = os.environ.get("GITHUB_JOB_STATUS", "unknown")
status_emoji = "✅ 성공" if status == "success" else "❌ 실패"

summary_path = "summary.json"
summary = {"passed": 0, "failed": 0, "skipped": 0}
try:
    with open(summary_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        summary["passed"] = len([t for t in data["tests"] if t["outcome"] == "passed"])
        summary["failed"] = len([t for t in data["tests"] if t["outcome"] == "failed"])
        summary["skipped"] = len([t for t in data["tests"] if t["outcome"] == "skipped"])
except Exception as e:
    print(f"⚠️ 요약 정보 읽기 실패: {e}")

summary_text = f"📊 테스트 결과: {summary['passed']} passed / {summary['failed']} failed / {summary['skipped']} skipped"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

device_info = {"deviceName": "unknown", "platformName": "unknown"}
try:
    with open("run_info.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                device_info[k] = v
except Exception as e:
    print(f"⚠️ 디바이스 정보 읽기 실패: {e}")

run_url = os.environ.get("GITHUB_RUN_URL", "#")

message = {
    "text": (
        f"{status_emoji}: Android 여신티켓 테스트 완료!\n"
        f"결과: {run_url}\n\n"
        f"{summary_text}\n\n"
        f"🕒 빌드 시간: {timestamp}\n"
        f"📱 디바이스: {device_info['deviceName']}\n"
        f"🤖 플랫폼: {device_info['platformName']}"
    )
}

res = requests.post(
    os.environ["SLACK_WEBHOOK_URL"],
    headers={"Content-Type": "application/json"},
    data=json.dumps(message)
)

try:
    print("Slack Webhook response:", res.json())
except Exception as e:
    print(f"⚠️ Slack 응답 파싱 실패: {e}")
    print(f"🔻 상태코드: {res.status_code}")
    print(f"🔻 응답본문: {res.text}")

