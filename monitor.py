import requests
import os

# 設定
MODEL = "MYD63J/A"  # iPhone 16 128GB Black
STORE = "R658"      # Apple 川崎
LINE_TOKEN = os.environ.get("LINE_TOKEN")

def check_inventory():
    url = f"https://www.apple.com/jp/shop/fulfillment-messages?parts.0={MODEL}&store={STORE}"
    
    # Appleのセキュリティを突破するための「最強の偽装ヘッダー」
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Referer": "https://www.apple.com/jp/shop/buy-iphone/iphone-16",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }
    
    session = requests.Session()
    
    try:
        print(f"Checking {MODEL} at {STORE}...")
        # タイムアウトを15秒に設定
        response = session.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            stores = data['body']['content']['pickupMessage']['stores']
            target_store = next((s for s in stores if s['storeNumber'] == STORE), None)
            
            if target_store:
                status = target_store['partsAvailability'][MODEL]['pickupDisplay']
                store_name = target_store['storeName']
                print(f"--- 判定成功 ---")
                print(f"店舗: {store_name} / 状況: {status}")
                
                if status == "available":
                    send_line(f"\n【在庫あり！】\n{store_name}で受け取り可能です。")
            else:
                print("店舗が見つかりませんでした。")
        else:
            print(f"Failed with Status: {response.status_code}")
            # 541が出る場合、AppleがこのサーバーIPを嫌っています
            if response.status_code == 541:
                print("Appleの強力なボット制限に接触中です。")
            
    except Exception as e:
        print(f"通信エラー: {e}")

def send_line(message):
    if not LINE_TOKEN:
        print("LINE通知をスキップしました（トークン未設定）")
        return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    payload = {"message": message}
    requests.post(url, headers=headers, data=payload)

if __name__ == "__main__":
    check_inventory()
