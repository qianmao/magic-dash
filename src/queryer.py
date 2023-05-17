
import requests

COIN_GECKO_SIMPLE_PRICE_URL = 'https://api.coingecko.com/api/v3/simple/price?ids={0}&vs_currencies={1}&include_24hr_change=true'
ME_API_COLLECTION_STATS_URL = 'https://api-mainnet.magiceden.dev/v2/collections/{0}/stats'

def query_coin_price_vol(symbol, currency):
    res = requests.get(COIN_GECKO_SIMPLE_PRICE_URL.format(symbol, currency)).json()
    # response example: {'bitcoin': {'usd': 50027, 'usd_24h_change': 1.0677771580989104}}
    return res[symbol][currency], res[symbol]['usd_24h_change']

def query_coin_price_vol_batch(symbols, currency):
    print(symbols)
    ids = ','.join(symbols)
    res = requests.get(COIN_GECKO_SIMPLE_PRICE_URL.format(ids, currency)).json()
    # response example: {'bitcoin': {'usd': 50027, 'usd_24h_change': 1.0677771580989104}}
    print(res)
    return res

def query_me_nft_collection_stats(symbol):
    res = requests.get(ME_API_COLLECTION_STATS_URL.format(symbol), headers={'Authorization': 'Bearer d1968b2f-064b-485d-83af-c074a0dee657'}).json()
    print(symbol)
    print(res)
    floorPrice = res['floorPrice'] if 'floorPrice' in res else None
    listedCount = res['listedCount'] if 'listedCount' in res else None
    avgPrice24hr = res['avgPrice24hr'] if 'avgPrice24hr' in res else None
    volumeAll = res['volumeAll'] if 'volumeAll' in res else None

    return symbol, floorPrice, listedCount,avgPrice24hr, volumeAll


