import json
import os
import requests
from datetime import datetime

# ✅ Slack Webhook URL from environment
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
GITHUB_REPO_URL = os.environ.get("GITHUB_REPO_URL", "")
GITHUB_RUN_ID = os.environ.get("GITHUB_RUN_ID", "")
GITHUB_JOB_STATUS = os.environ.get("GITHUB_JOB_STATUS", "failure")

status_emoji = "✅ 성공" if GITHUB_JOB_STATUS.lower() == "success" else "❌ 실패"

# 📊 테스트 요약
summary = {"passed": 0, "failed": 0, "skipped": 0}
try:
    with open("C:/Users/WW/Desktop/workspace/00. src/appium-pytest-template/summary.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        summary["passed"] = len([t for t in data["tests"] if t["outcome"] == "passed"])
        summary["failed"] = len([t for t in data["tests"] if t["outcome"] == "failed"])
        summary["skipped"] = len([t for t in data["tests"] if t["outcome"] == "skipped"])
except Exception as e:
    print(f"⚠️ 요약 정보 읽기 실패: {e}")

summary_text = f"📊 테스트 결과: {summary['passed']} passed / {summary['failed']} failed / {summary['skipped']} skipped"

# 🕒 빌드 시간
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 📱 디바이스 정보
device_info = {"deviceName": "unknown", "platformName": "unknown"}
try:
    with open("C:/Users/WW/Desktop/workspace/00. src/appium-pytest-template/run_info.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                device_info[k] = v
except Exception as e:
    print(f"⚠️ 디바이스 정보 읽기 실패: {e}")

# Slack 메시지 생성
message = {
    "text": (
        f"{status_emoji}: Android 여신티켓 테스트 완료!\n"
        f"🔗 결과: {GITHUB_REPO_URL}/actions/runs/{GITHUB_RUN_ID}\n\n"
        f"{summary_text}\n\n"
        f"🕒 빌드 시간: {timestamp}\n"
        f"📱 디바이스: {device_info['deviceName']}\n"
        f"🤖 플랫폼: {device_info['platformName']}"
    )
}

res = requests.post(
    SLACK_WEBHOOK_URL,
    headers={"Content-Type": "application/json"},
    data=json.dumps(message)
)
print("Slack Webhook response:", res.json())
