from flask import Flask, request, redirect
import geoip2.database

app = Flask(__name__)

# 載入 GeoIP2 資料庫
reader = geoip2.database.Reader('./GeoLite2-Country.mmdb')

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent', '').lower()
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    query_string = request.query_string.decode()

    # 預設值
    country_code = 'Unknown'

    # 嘗試解析國家
    try:
        response = reader.country(ip_address)
        country_code = response.country.iso_code  # e.g. 'TW'
    except:
        pass

    # 判斷是否為 Facebook Crawler
    is_facebook_crawler = "facebookexternalhit" in user_agent or "facebot" in user_agent

    # Log 印出來方便你在 Render 上 debug
    print(f"訪客 IP: {ip_address}, 國家: {country_code}, UA: {user_agent}")

    # 條件跳轉邏輯
    if is_facebook_crawler or country_code not in ['TW', 'Unknown']:
        return redirect("https://1xbetw.mystrikingly.com/?" + query_string, code=302)
    else:
        return redirect("https://bit.ly/1XBET-VIP?" + query_string, code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




