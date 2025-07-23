import os
import glob
import requests
import sys

# Windows 출력 인코딩 설정 (Unicode 오류 방지용)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# 스크린샷 파일 찾기
file_list = glob.glob("**/screenshots/failure_*.png", recursive=True)
if not file_list:
    print("❗ No screenshot found")
    exit(0)

filepath = file_list[0]
print(f"📸 Uploading screenshot: {filepath}")

# 환경변수 체크
slack_token = os.environ.get("SLACK_TOKEN")
slack_channel = os.environ.get("SLACK_CHANNEL")

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
            "initial_comment": "❌ 테스트 실패 - 실행 스크린샷 첨부",
            "filename": os.path.basename(filepath),
        },
    )

# 응답 처리
try:
    json_res = res.json()
    if json_res.get("ok"):
        print("✅ 스크린샷이 Slack에 성공적으로 업로드되었습니다.")
    else:
        print(f"❗ 파일 업로드 실패: {json_res}")
except Exception as e:
    print("❗ Slack 응답 파싱 실패:", e)
    print("응답 상태코드:", res.status_code)
    print("응답 본문:", res.text)
