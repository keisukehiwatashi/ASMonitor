import requests
import os

# 設定
MODEL = "MYD63J/A"  # iPhone 16 128GB Black
STORE = "R658"      # Apple 川崎
LINE_TOKEN = os.environ.get("LINE_TOKEN")

def check_inventory():
    # Appleのトップページを一度踏むような設定にして、より人間らしくします
    url = f"https://www.apple.com/jp/shop/fulfillment-messages?parts.0={MODEL}&store={STORE}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
        "Accept": "*/*",
        "Accept-Language": "ja-JP,ja;q=0.9",
        "Referer": "https://www.apple.com/jp/shop/buy-iphone/iphone-16",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    # セッション（Cookieを保持する仕組み）を使って通信
    session = requests.Session()
    
    try:
        print(f"Checking inventory for {MODEL} at {STORE}...")
        # タイムアウトを少し長めに設定
        response = session.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"Apple Server Error: {response.status_code}")
            # 541が出た場合でも、レスポンスの内容を少し表示してヒントを探る
            print(f"Response snippet: {response.text[:100]}")
            return

        data = response.json()
        stores = data['body']['content']['pickupMessage']['stores']
        target_store = next((s for s in stores if s['storeNumber'] == STORE), None)
        
        if target_store:
            status = target_store['partsAvailability'][MODEL]['pickupDisplay']
            store_name = target_store['storeName']
            print(f"--- 判定結果 ---")
            print(f"店舗: {store_name} / 状況: {status}")
            
            if status == "available":
                send_line(f"\n【在庫あり！】\n{store_name}で受け取り可能です！")
        else:
            print("店舗が見つかりませんでした。")
            
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
