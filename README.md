# Magic Dash
Degens like you love metrics - real time metrics. You definitely don't want to miss a hot coin, an NFT drop, or an early warning of a collapse. As a result, I ended up building this dash: [![Watch the video](https://i.imgur.com/e5uez3r.png)](https://twitter.com/i/status/1493438302472470529)[click to watch the video](https://twitter.com/i/status/1493438302472470529)

## Features
* Display metrics for coins supported by [CoinMarketCap](coinmarketcap)
* Display metrics for NFT collections supported by [MagicEden](https://magiceden.io/). SOL collections only at the moment.

## Roadmap
### General
* Web UI for easy configuration
* Twitter real-time tracking
* Custom alerts
* Programtic trading

### Web3
* ETH NFT collection support
* Wallet connect for one-click configuration
* Web3 breaking news

### Web2
* Stock price support
* Finance breaking news

## Deployment
* Add following in crontab
```
@reboot sudo chmod 777 [BASE_DIR]/magic-dash/src/images_to_display
@reboot sudo python3 [BASE_DIR]/magic-dash/src/display_main.py
*/5 * * * * sudo python3 /home/pi/magic-dash/src/refresher.py
```