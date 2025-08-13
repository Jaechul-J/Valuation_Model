import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Create a session with retry logic
session = requests.Session()
retry = Retry(
    total=5,               # Retry up to 5 times
    backoff_factor=1,      # Wait 1s, 2s, 4s...
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"]
)
session.mount("https://", HTTPAdapter(max_retries=retry))

# Browser-like headers to avoid bot detection
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
    "Referer": "https://finance.naver.com/"
}

def get_year_end_price(stock_code, year):
    """
    네이버 금융에서 특정 연도의 마지막 거래일 종가를 가져옴
    """
    code = str(stock_code).zfill(6)  # 6자리 코드로 변환
    url = f"https://finance.naver.com/item/sise_day.nhn?code={code}"

    for page in range(1, 25):  # 최대 25페이지 검색
        try:
            res = session.get(f"{url}&page={page}", headers=headers, timeout=10)
            res.raise_for_status()  # HTTP error check
        except requests.exceptions.RequestException as e:
            print(f"⚠️ {code} 페이지 {page} 요청 실패: {e}")
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.select("table.type2 tr")

        for row in rows[2:]:
            cols = row.select("td")
            if len(cols) < 2:
                continue

            date_str = cols[0].text.strip()
            close_str = cols[1].text.strip().replace(",", "")

            if not date_str or not close_str:
                continue

            try:
                date = datetime.strptime(date_str, "%Y.%m.%d")
                close_price = int(close_str)

                if date.year == year:
                    return close_price  # 첫 번째 해당 연도 데이터 반환
            except ValueError:
                continue
    return None

def fetch_all_prices(financial_csv_path, output_path):
    df = pd.read_csv(financial_csv_path, encoding="utf-8-sig")
    codes = df["stock_code"].dropna().unique()
    year = df["year"].max()

    price_records = []
    for code in codes:
        price = get_year_end_price(code, year)
        if price:
            print(f"✅ {code} {year}: {price}")
            price_records.append({"stock_code": code, "year": year, "year_end_price": price})
        else:
            print(f"❌ {code} {year}: Price not found")
        time.sleep(1.5)  # 요청 간 간격을 늘려 차단 방지

    prices_df = pd.DataFrame(price_records)
    prices_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"💾 저장 완료: {output_path}")

if __name__ == "__main__":
    fetch_all_prices(
        "data/processed/financial_summary.csv",
        "data/processed/stock_prices.csv"
    )