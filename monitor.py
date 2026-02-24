import requests

# --- 設定 ---
# テスト用: iPhone 16 128GB Black (日本モデル)
# iPhone 17発売後は、ここを新しい型番に書き換えます
MODEL = "MYD63J/A" 
STORE = "R658"  # Apple 川崎

def check_inventory():
    # Apple公式の在庫確認API
    url = f"https://www.apple.com/jp/shop/fulfillment-messages?parts.0={MODEL}&store={STORE}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # 店舗データの抽出
        stores = data['body']['content']['pickupMessage']['stores']
        # リストの中から「川崎 (R658)」を探す
        target_store = next((s for s in stores if s['storeNumber'] == STORE), None)
        
        if target_store:
            store_name = target_store['storeName']
            # 在庫ステータス (available = 在庫あり)
            status = target_store['partsAvailability'][MODEL]['pickupDisplay']
            
            print(f"--- 判定結果 ---")
            print(f"店舗: {store_name}")
            print(f"在庫状況: {status}")
            
            if status == "available":
                print("★【在庫あり】今すぐ購入可能です！")
            else:
                print("×【在庫なし】")
        else:
            print(f"エラー: 店舗コード {STORE} が見つかりませんでした。")
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    check_inventory()
