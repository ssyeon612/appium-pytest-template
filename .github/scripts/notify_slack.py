import os, json, requests, sys
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

slack_token = os.environ.get("SLACK_TOKEN")
slack_channel = os.environ.get("SLACK_CHANNEL")
job_status = os.environ.get("GITHUB_JOB_STATUS", "unknown")
run_url = os.environ.get("GITHUB_RUN_URL")
repository = os.environ.get("GITHUB_REPOSITORY")

status_emoji = "✅ 성공" if job_status == "success" else "❌ 실패"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

summary = {"passed": 0, "failed": 0, "skipped": 0}
try:
    with open("summary.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for t in data["tests"]:
            summary[t["outcome"]] += 1
except Exception as e:
    print("[경고] summary.json 읽기 실패:", e)

device_info = {"deviceName": "unknown", "platformName": "unknown"}
try:
    with open("run_info.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                device_info[k] = v
except Exception as e:
    print("[경고] run_info.txt 읽기 실패:", e)

message = {
    "channel": slack_channel,
    "text": (
        f"{status_emoji}: Android 여신티켓 테스트 완료!\n"
        f"결과: {run_url}\n\n"
        f"📊 테스트 결과: {summary['passed']} passed / {summary['failed']} failed / {summary['skipped']} skipped\n\n"
        f"🕒 빌드 시간: {timestamp}\n"
        f"📱 디바이스: {device_info['deviceName']}\n"
        f"🤖 플랫폼: {device_info['platformName']}"
    )
}

try:
    res = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {slack_token}",
            "Content-Type": "application/json"
        },
        data=json.dumps(message)
    )
    print("Slack 응답:", res.json())
except Exception as send_err:
    print("❌ Slack 메시지 전송 실패:", send_err)
