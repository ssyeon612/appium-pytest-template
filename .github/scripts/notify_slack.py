import json, os, requests, sys
from datetime import datetime

# Windows 환경에서 유니코드 출력을 위해 인코딩 설정
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass  # GitHub Actions PowerShell에서는 무시해도 됨

status_emoji = "✅ 성공" if os.environ.get("GITHUB_JOB_STATUS") == "success" else "❌ 실패"

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

# 빌드 시간
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

# Slack 메시지 구성
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

# Slack Webhook 요청
try:
    res = requests.post(
        os.environ["SLACK_WEBHOOK_URL"],
        headers={"Content-Type": "application/json"},
        data=json.dumps(message)
    )
    try:
        print("Slack Webhook 응답:", res.json())
    except Exception as parse_err:
        print("[경고] Slack 응답 파싱 실패:", parse_err)
        print("응답 상태코드:", res.status_code)
        print("응답 본문:", res.text)
except Exception as send_err:
    print("[에러] Slack 메시지 전송 실패:", send_err)
