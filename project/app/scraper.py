import requests

LCW_API_URL = 'https://api.livecoinwatch.com/coins/list'
API_KEY = 'f4ab5197-3ae3-4b23-afb1-12866208337e'



def scrape_crypto_table():
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY
    }

    payload = {
        'currency': 'USD',
        'sort': 'rank',
        'order': 'ascending',
        'offset': 0,
        'limit': 100,  # You can increase this up to 500 if needed
        'meta': True
    }

    try:
        response = requests.post(LCW_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        coins = response.json()
    except requests.RequestException as e:
        print("Error fetching data from LiveCoinWatch:", e)
        return []

    crypto_data = []

    for coin in coins:
        crypto_data.append({
            'name': coin.get('name'),
            'code': coin.get('code'),
            'price': f"{coin.get('rate', 0):,.2f}",
            # 'market_cap': coin.get('marketCap', 0),
            'volume_24h': coin.get('volume', 0),
            # 'ath': coin.get('allTimeHigh', 0)
        })

    return crypto_data