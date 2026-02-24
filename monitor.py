import requests
import os

# 設定
MODEL = "MYD63J/A"  # iPhone 16 128GB Black
STORE = "R658"      # Apple 川崎
LINE_TOKEN = os.environ.get("LINE_TOKEN")

def check_inventory():
    url = f"https://www.apple.com/jp/shop/fulfillment-messages?parts.0={MODEL}&store={STORE}"
    
    # ブラウザからのアクセスに見せかけるための魔法の言葉 (User-Agent)
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    }
    
    try:
        print(f"Checking inventory for {MODEL} at {STORE}...")
        response = requests.get(url, headers=headers, timeout=10)
        
        # 503エラーなどが出た場合に詳細を表示
        if response.status_code != 200:
            print(f"Apple Server Returned Error: {response.status_code}")
            return

        data = response.json()
        stores = data['body']['content']['pickupMessage']['stores']
        target_store = next((s for s in stores if s['storeNumber'] == STORE), None)
        
        if target_store:
            status = target_store['partsAvailability'][MODEL]['pickupDisplay']
            store_name = target_store['storeName']
            print(f"--- 判定結果 ---")
            print(f"店舗: {store_name}")
            print(f"在庫状況: {status}")
            
            if status == "available":
                send_line(f"\n【在庫あり！】\n{store_name}で受け取り可能です！")
        else:
            print("店舗データが見つかりませんでした。")
            
    except Exception as e:
        print(f"通信エラーが発生しました: {e}")

def send_line(message):
    if not LINE_TOKEN:
        print("LINE_TOKENが設定されていないため、通知をスキップしました。")
        return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    payload = {"message": message}
    requests.post(url, headers=headers, data=payload)

if __name__ == "__main__":
    check_inventory()
