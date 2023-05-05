
import requests

COIN_GECKO_SIMPLE_PRICE_URL = 'https://api.coingecko.com/api/v3/simple/price?ids={0}&vs_currencies={1}&include_24hr_change=true'
ME_API_COLLECTION_STATS_URL = 'https://api-mainnet.magiceden.dev/v2/collections/{0}/stats'

def _query_crypto(symbol, currency):
	res = requests.get(COIN_GECKO_SIMPLE_PRICE_URL.format(symbol, currency))
	# response example: {'bitcoin': {'usd': 50027, 'usd_24h_change': 1.0677771580989104}}
	return res.json()

def query_btc_usd():
	res = _query_crypto('bitcoin', 'usd')
	return res['bitcoin']['usd'], res['bitcoin']['usd_24h_change']

def query_eth_usd():
	res = _query_crypto('ethereum', 'usd')
	return res['ethereum']['usd'], res['ethereum']['usd_24h_change']

def query_doge_usd():
	res = _query_crypto('dogecoin', 'usd')
	return res['dogecoin']['usd'], res['dogecoin']['usd_24h_change']

def query_omg_usd():
	res = _query_crypto('omisego', 'usd')
	return res['omisego']['usd'], res['omisego']['usd_24h_change']

def query_nkn_usd():
	res = _query_crypto('nkn', 'usd')
	return res['nkn']['usd'], res['nkn']['usd_24h_change']

def query_shib_usd():
	res = _query_crypto('shiba-inu', 'usd')
	return res['shiba-inu']['usd'], res['shiba-inu']['usd_24h_change']

def query_sol_usd():
        res = _query_crypto('solana', 'usd')
        return res['solana']['usd'], res['solana']['usd_24h_change']

def query_me_nft_collection_stats(symbol):
        res = requests.get(ME_API_COLLECTION_STATS_URL.format(symbol), headers={'Authorization': 'Bearer d1968b2f-064b-485d-83af-c074a0dee657'}).json()
        print(symbol)
        print(res)
        floorPrice = res['floorPrice'] if 'floorPrice' in res else None
        listedCount = res['listedCount'] if 'listedCount' in res else None
        avgPrice24hr = res['avgPrice24hr'] if 'avgPrice24hr' in res else None
        volumeAll = res['volumeAll'] if 'volumeAll' in res else None

        return symbol, floorPrice, listedCount,avgPrice24hr, volumeAll


