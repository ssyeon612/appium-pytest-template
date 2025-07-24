import os, glob, json, requests, sys
from datetime import datetime

# 콘솔 인코딩 설정
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# 환경변수 읽기
slack_token = os.environ.get("SLACK_TOKEN")
slack_channel = os.environ.get("SLACK_CHANNEL")

if not slack_token or not slack_channel:
    print("❗ SLACK_TOKEN 또는 SLACK_CHANNEL 환경변수가 없습니다.")
    sys.exit(1)

# 스크린샷 파일 탐색
file_list = glob.glob("**/screenshots/failure_*.png", recursive=True)
if not file_list:
    print("❗ 스크린샷 없음. 종료.")
    sys.exit(0)

# 최신 순 정렬 후 오래된 항목 정리
file_list.sort(key=os.path.getmtime, reverse=True)
max_keep = 5
for old_file in file_list[max_keep:]:
    try:
        os.remove(old_file)
        print(f"🧹 오래된 스크린샷 삭제됨: {old_file}")
    except Exception as e:
        print(f"⚠️ 삭제 실패: {old_file} - {e}")

# 최신 스크린샷 하나 선택
filepath = file_list[0]
filename = os.path.basename(filepath)
file_size = int(os.path.getsize(filepath))

print(f"📸 Uploading screenshot: {filepath}")
print(f"▶️ filename: {filename}, filesize: {file_size}")

# Step 1: 업로드 URL 요청
headers = {
    "Authorization": f"Bearer {slack_token}",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "filename": filename,
    "length": file_size
}
res = requests.post("https://slack.com/api/files.getUploadURLExternal", headers=headers, data=data)

try:
    res_json = res.json()
except Exception:
    print("❗ 응답 파싱 실패:", res.text)
    sys.exit(1)

if not res_json.get("ok"):
    print("❗ upload URL 요청 실패:", res_json)
    sys.exit(1)

upload_url = res_json["upload_url"]
file_id = res_json["file_id"]
print(f"✅ 업로드 URL 수신: {upload_url}")

# Step 2: PUT 요청으로 파일 업로드
with open(filepath, "rb") as f:
    put_res = requests.post(upload_url, data=f)

if put_res.status_code != 200:
    print("❗ 파일 업로드 실패 (PUT):", put_res.status_code, put_res.text)
    sys.exit(1)

# Step 3: 업로드 완료 처리
headers["Content-Type"] = "application/json; charset=utf-8"
complete_payload = {
    "files": [{
        "id": file_id,
        "title": f"테스트 실패 스크린샷 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }],
    "channel_id": slack_channel
}

complete_res = requests.post(
    "https://slack.com/api/files.completeUploadExternal",
    headers=headers,
    json=complete_payload
)

complete_json = complete_res.json()
if complete_json.get("ok"):
    print("✅ 스크린샷 업로드 성공!")
else:
    print("❗ 완료 단계 실패:", complete_json)
