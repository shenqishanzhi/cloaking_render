from flask import Flask, request, redirect
import geoip2.database

app = Flask(__name__)

# 讀取 GeoLite2 資料庫
reader = geoip2.database.Reader('./GeoLite2-Country.mmdb')

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent', '').lower()
    ip_address = request.remote_addr
    query_string = request.query_string.decode()

    # 嘗試從 IP 判斷國家
    try:
        response = reader.country(ip_address)
        country_code = response.country.iso_code  # e.g. 'TW'
    except:
        country_code = 'Unknown'

    # 判斷是否為 Facebook 審核機器人
    is_facebook_crawler = "facebookexternalhit" in user_agent or "facebot" in user_agent

    # ✅ 條件判斷：如果是審核機器人 or 非台灣 IP → 跳白頁
    if is_facebook_crawler or country_code != 'TW':
        return redirect("https://1xbettw.mystrikingly.com/" + query_string, code=302)
    else:
        return redirect("https://bit.ly/1XBET-VIP" + query_string, code=302)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)




