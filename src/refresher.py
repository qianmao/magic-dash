import display_utils
import os
import queryer
import time
import json

from PIL import Image


ME_NFT_COLLECTION_ICON_IMAGE = {
    'monkelabs': 'https://cdn.magiceden.io/rs:fill:320:320:0:0/plain/https://dl.airtable.com/.attachmentThumbnails/37fd1a44d683784b3b6195f0e5dec266/8196493e',
    'boryoku_dragonz': 'https://cdn.magiceden.io/rs:fill:640:640:0:0/plain/https://arweave.net/HZnIqVCuYGmbevPtdKtfDStvqax7DmojdQyKL68qdaY?ext=png',
    'thugbirdz': 'https://www.arweave.net/nGvadeW0UuvIgzZUyNKaQ-c8400CDQn1FwNthOJ_KUw?ext=png',
    'trippin_ape_tribe': 'https://i.imgur.com/iFgvQva.png',
    'okay_bears': 'https://bafkreidgfsdjx4nt4vctch73hcchb3pkiwic2onfw5yr4756adchogk5de.ipfs.dweb.link/',
    'degods': 'https://i.imgur.com/fO3tI1t.png',
    'suteki': 'https://img-cdn.magiceden.dev/rs:fill:400:400:0:0/plain/https://dl.airtable.com/.attachmentThumbnails/bb5f40a7c3d9feb5c27e4810e83e1f74/1f770b7f'
}

ME_NFT_COLLECTION_NAME = {
    'monkelabs': 'MonkeLabs',
    'boryoku_dragonz': 'Boryoku Dragonz',
    'thugbirdz': 'Thugbirdz',
    'trippin_ape_tribe': "Trippin' Ape Tribe",
    'okay_bears': 'Okay Bears',
    'degods': 'DeGods',
    'suteki': 'Suteki'
}

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = '{0}/{1}'.format(CURRENT_DIR_PATH, 'config.json')
IMAGE_TO_DISPLAY_DIR = '{0}/{1}'.format(CURRENT_DIR_PATH, 'images_to_display')

LAMPORT_PER_SOL = 1000000000.0

def _get_or_default(d, *keys, default=None):
    try:
        for k in keys:
            d = d[k]
    except (KeyError, IndexError):
        return default
    return d

if __name__ == "__main__":
    with open(CONFIG_FILE) as f:
        config = json.load(f);
        crypto_monitoring_list = _get_or_default(config, 'monitoringList', 'crypto') or []
        nft_collection_monitoring_list = [] #_get_or_default(config, 'monitoringList', 'nft', 'collection') or []

        if len(crypto_monitoring_list) == 0 and len(nft_collection_monitoring_list) == 0:
            quit() 

        total_width = 0
        image_list = []
            
        for crypto in crypto_monitoring_list:
           price, pct_change = queryer.query_coin_price_vol(crypto['symbol'], crypto['currency'])
           print(price, pct_change)
           image = display_utils.format_crypto_display(crypto['displayName'], crypto['logoFile'], price, pct_change)
           image_list.append(image)
           total_width += image.width
   
        if len(nft_collection_monitoring_list) > 0:
            image = display_utils.format_magiceden_logo()
            image_list.append(image)
            total_width += image.width
           
            image = display_utils.add_buffer(16)
            image_list.append(image)
            total_width += image.width

            # funcs = CRYPTO_SYMBOL_FUNC_DICT['sol/usd']
            # price, pct_change = funcs[0]()
            # image = funcs[1](price, pct_change)
            # image_list.append(image)
            # total_width += image.width
   

            # image = display_utils.add_buffer(16)
            # image_list.append(image)
            # total_width += image.width
            
            # image = display_utils.format_nyancat()
            # image_list.append(image)
            # total_width += image.width

        for collection in nft_collection_monitoring_list:
            symbol = collection.lower()
            symbol, floorPrice, listedCount, avgPrice24hr, volumeAll = queryer.query_me_nft_collection_stats(symbol)
            imageUrl = ME_NFT_COLLECTION_ICON_IMAGE[symbol]
            image = display_utils.format_me_nft_collection_stats_display(ME_NFT_COLLECTION_NAME[symbol], floorPrice / LAMPORT_PER_SOL if floorPrice else None, avgPrice24hr / LAMPORT_PER_SOL if avgPrice24hr else None, volumeAll / LAMPORT_PER_SOL if volumeAll else None, imageUrl)
            image_list.append(image)
            total_width += image.width

  #      for crypto in crypto_monitoring_list:
  #          funcs = CRYPTO_SYMBOL_FUNC_DICT[crypto.lower()]
  #          price, pct_change = funcs[0]()
  #          image = funcs[1](price, pct_change)
  #          image_list.append(image)
  #          total_width += image.width
   

        merged_image = Image.new('RGB', (total_width, 32))
        current_width = 0

        for image in image_list:
            merged_image.paste(image, (current_width, 0))
            current_width += image.width

        file_path = '{0}/{1}.pcx'.format(IMAGE_TO_DISPLAY_DIR, round(time.time()))
        merged_image.save(file_path)
