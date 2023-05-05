import os
import requests

from io import BytesIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

WHITE = (255, 255, 255)
GREEN = (25, 255, 25)
RED = (255, 0, 0)
PINK = (176, 38, 255)

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

LARGE_FONT_FILE = '{0}/{1}'.format(CURRENT_DIR_PATH, 'fonts/7x14.pil')
LARGE_FONT = ImageFont.load(LARGE_FONT_FILE)
LARGE_FONT_WIDTH = 7

SMALL_FONT_FILE = '{0}/{1}'.format(CURRENT_DIR_PATH, 'fonts/5x8.pil')
SMALL_FONT = ImageFont.load(SMALL_FONT_FILE)
SMALL_FONT_WIDTH = 5

def _format_crypto_display(symbol, logo_file, price, pct_change, price_round=3, pct_change_round=2):
    logo_file = '{0}/{1}/{2}'.format(CURRENT_DIR_PATH, 'logo', logo_file)
    icon_image = Image.open(logo_file).convert('RGB')

    headline = symbol
    headline_width = len(headline) * LARGE_FONT_WIDTH
    headline_image = Image.new('RGB', (headline_width, 16))
    ImageDraw.Draw(headline_image).text((0, 0), headline, font=LARGE_FONT, fill=WHITE)

    price = price if round(price, price_round) == round(price, price_round) else round(price, price_round)
    price_line = '{0}'.format(price)
    price_line_width = len(price_line) * LARGE_FONT_WIDTH
    price_line_color = GREEN if pct_change >= 0 else RED
    price_line_image = Image.new('RGB', (price_line_width, 16))
    ImageDraw.Draw(price_line_image).text((0, 0), price_line, font=LARGE_FONT, fill=price_line_color)

    pct_change_line = u'{0}{1}%'.format('+' if pct_change >= 0 else '', round(pct_change, pct_change_round))
    pct_change_line_width = len(pct_change_line) * SMALL_FONT_WIDTH
    pct_change_line_color = GREEN if pct_change >= 0 else RED
    pct_change_line_image = Image.new('RGB', (pct_change_line_width, 16))
    ImageDraw.Draw(pct_change_line_image).text((0, 0), pct_change_line, font=SMALL_FONT, fill=pct_change_line_color)

    text_image_width = max(headline_image.width, price_line_image.width + pct_change_line_image.width + 4)

    text_image = Image.new('RGB', (text_image_width, 32))
    text_image.paste(headline_image, (0, 0))
    text_image.paste(price_line_image, (0, 16))
    text_image.paste(pct_change_line_image, (price_line_image.width + 4, 19))

    buffer_width = 8

    image = Image.new('RGB', (buffer_width + icon_image.width + text_image.width + buffer_width, 32))
    image.paste(icon_image, (buffer_width, 0))
    image.paste(text_image, (buffer_width + icon_image.width + buffer_width, 0))

    return image


def format_btc_usd_display(price, pct_change):
    return _format_crypto_display('BTC/USD', 'btc-logo_32x32.png', price, pct_change)

def format_eth_usd_display(price, pct_change):
    return _format_crypto_display('ETH/USD', 'eth-logo_32x32.png', price, pct_change)

def format_doge_usd_display(price, pct_change):
    return _format_crypto_display('DOGE/USD', 'doge-logo_32x32.png', price, pct_change)

def format_omg_usd_display(price, pct_change):
    return _format_crypto_display('OMG/USD', 'omg-logo_32x32.png', price, pct_change)

def format_nkn_usd_display(price, pct_change):
    return _format_crypto_display('NKN/USD', 'nkn-logo_32x32.png', price, pct_change)

def format_shib_usd_display(price, pct_change):
    return _format_crypto_display('SHIB/USD', 'shib-logo_32x32.png', price, pct_change, price_round=7)

def format_sol_usd_display(price, pct_change):
    return _format_crypto_display('SOL/USD', 'sol-logo_32x32.png', price, pct_change)

def format_magiceden_logo():
    logo_file = '{0}/{1}/{2}'.format(CURRENT_DIR_PATH, 'logo', 'magiceden-full-logo.png')
    image = Image.open(logo_file).resize((170, 32)).convert('RGB')
    return image

def format_nyancat():
    f = '{0}/{1}/{2}'.format(CURRENT_DIR_PATH, 'logo', 'nyan-cat.png')
    image = Image.open(f).resize((114,32)).convert('RGB')
    return image

def add_buffer(width):
    image = Image.new('RGB', (width, 32))
    return image

def format_me_nft_collection_stats_display(symbol, floorPrice, avgPrice24hr, volumeAll, imageUrl, numRound=2):
    res = requests.get(imageUrl)
    icon_image = Image.open(BytesIO(res.content)).resize((32, 32)).convert('RGB')
 
    headline = symbol
    headline_width = len(headline) * LARGE_FONT_WIDTH
    headline_image = Image.new('RGB', (headline_width, 16))
    ImageDraw.Draw(headline_image).text((0, 0), headline, font=LARGE_FONT, fill=PINK)   

    details_line = ''

    if floorPrice:
        details_line += 'Flr {0}'.format(round(floorPrice, numRound))
    
    if avgPrice24hr:
        details_line += ' Avg {0}'.format(round(avgPrice24hr, numRound))
    details_line_width = len(details_line) * LARGE_FONT_WIDTH
    details_line_image = Image.new('RGB', (details_line_width, 16))
    ImageDraw.Draw(details_line_image).text((0,0), details_line, font=LARGE_FONT, fill=GREEN)

    text_image_width = max(headline_image.width, details_line_image.width)

    buffer_width = 8
    image = Image.new('RGB', (buffer_width + icon_image.width + text_image_width + buffer_width, 32))
    image.paste(icon_image, (buffer_width, 0))
    image.paste(headline_image, (buffer_width + icon_image.width + buffer_width, 0))
    image.paste(details_line_image, (buffer_width + icon_image.width + buffer_width, 16))


    return image

