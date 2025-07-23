import json, os, requests, sys
from datetime import datetime

# Windows 인코딩 대응
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass  # PowerShell 환경에선 무시해도 됨

# ✅ 테스트 상태 이모지
status = os.environ.get("GITHUB_JOB_STATUS", "").lower()
status_emoji = "✅ 성공" if status == "success" else "❌ 실패"

# ✅ 테스트 요약 정보
summary = {"passed": 0, "failed": 0, "skipped": 0}
try:
    with open("summary.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        summary["passed"] = len([t for t in data.get("tests", []) if t.get("outcome") == "passed"])
        summary["failed"] = len([t for t in data.get("tests", []) if t.get("outcome") == "failed"])
        summary["skipped"] = len([t for t in data.get("tests", []) if t.get("outcome") == "skipped"])
except Exception as e:
    print(f"[경고] summary.json 읽기 실패: {e}")

# ✅ 디바이스 정보
device_info = {"deviceName": "unknown", "platformName": "unknown"}
try:
    with open("run_info.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                device_info[k.strip()] = v.strip()
except Exception as e:
    print(f"[경고] run_info.txt 읽기 실패: {e}")

# ✅ 빌드 시간
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ✅ Slack 메시지 구성
message = {
    "text": (
        f"{status_emoji}: Android 여신티켓 테스트 완료!\n"
        f"결과: https://github.com/{os.environ.get('GITHUB_REPOSITORY')}/actions/runs/{os.environ.get('GITHUB_RUN_ID')}\n\n"
        f"📊 테스트 결과: {summary['passed']} passed / {summary['failed']} failed / {summary['skipped']} skipped\n\n"
        f"🕒 빌드 시간: {timestamp}\n"
        f"📱 디바이스: {device_info['deviceName']}\n"
        f"🤖 플랫폼: {device_info['platformName']}"
    )
}

# ✅ Slack Webhook 전송
try:
    res = requests.post(
        os.environ["SLACK_WEBHOOK_URL"],
        headers={"Content-Type": "application/json"},
        data=json.dumps(message)
    )
    print("Slack Webhook 응답 상태코드:", res.status_code)
    print("Slack Webhook 응답 본문:", res.text)
except Exception as send_err:
    print("[에러] Slack 메시지 전송 실패:", send_err)
