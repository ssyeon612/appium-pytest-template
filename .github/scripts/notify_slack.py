import json
import os
import requests
import sys
from datetime import datetime

# 유니코드 출력 처리 (Windows 환경 대응)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

status_emoji = "✅ 성공" if os.environ.get("GITHUB_JOB_STATUS") == "success" else "❌ 실패"
run_url = os.environ.get("GITHUB_RUN_URL", "URL 없음")

# 테스트 요약
summary = {"passed": 0, "failed": 0, "skipped": 0}
try:
    with open("summary.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        summary["passed"] = len([t for t in data["tests"] if t["outcome"] == "passed"])
        summary["failed"] = len([t for t in data["tests"] if t["outcome"] == "failed"])
        summary["skipped"] = len([t for t in data["tests"] if t["outcome"] == "skipped"])
except Exception as e:
    print(f"[경고] summary.json 읽기 실패: {e}")

# 디바이스 정보
device_info = {"deviceName": "unknown", "platformName": "unknown"}
try:
    with open("run_info.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                device_info[k] = v
except Exception as e:
    print(f"[경고] run_info.txt 읽기 실패: {e}")

# Slack Webhook 메시지 전송
message = {
    "text": (
        f"{status_emoji}: Android 여신티켓 테스트 완료!\n"
        f"결과: {run_url}\n\n"
        f"📊 테스트 결과: {summary['passed']} passed / {summary['failed']} failed / {summary['skipped']} skipped\n\n"
        f"🕒 빌드 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"📱 디바이스: {device_info['deviceName']}\n"
        f"🤖 플랫폼: {device_info['platformName']}"
    )
}

try:
    res = requests.post(
        os.environ["SLACK_WEBHOOK_URL"],
        headers={"Content-Type": "application/json"},
        data=json.dumps(message)
    )
    try:
        print("✅ Slack Webhook 응답:", res.json())
    except Exception as e:
        print("⚠️ Slack 응답 파싱 실패:", e)
        print("응답 상태코드:", res.status_code)
        print("응답 본문:", res.text)
except Exception as send_err:
    print("❌ Slack 메시지 전송 실패:", send_err)
