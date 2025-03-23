
import requests
import schedule
import time
from bs4 import BeautifulSoup

# 你的 Slack Webhook URL（記得改成你的網址）
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# 記錄上一次的活動數量
last_activity_count = 0

def check_taishin_bank():
    global last_activity_count
    url = "https://www.taishinbank.com.tw/TSB/personal/common/bonus/"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 找出活動列表（這裡的 class 需要根據網頁實際 HTML 結構調整）
        activities = soup.select(".event-item")  # 這可能需要修改

        if not activities:
            print("沒有找到活動")
            return
        
        # 目前活動數量
        current_activity_count = len(activities)
        
        # 如果有新活動，發送通知到 Slack
        if current_activity_count > last_activity_count:
            message = f"臺新銀行有新的數位券活動！目前總共有 {current_activity_count} 個活動。\n查看頁面: {url}"
            send_to_slack(message)
        
        # 更新活動數量
        last_activity_count = current_activity_count
    
    except requests.exceptions.RequestException as e:
        print(f"錯誤: {e}")

def send_to_slack(message):
    """ 發送訊息到 Slack """
    payload = {"text": message}
    requests.post(SLACK_WEBHOOK_URL, json=payload)

# 每小時執行一次
schedule.every(1).hours.do(check_taishin_bank)

print("開始監測臺新銀行數位券活動...")
while True:
    schedule.run_pending()
    time.sleep(10)





