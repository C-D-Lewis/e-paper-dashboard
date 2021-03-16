# e-paper-frame

E-paper photo frame Python app for Waveshare 7.5in V2 e-paper display with
information widgets.

![](photo.jpg)

Included widgets:

* Time and date
* Current weather - type, temperature, day high/low, chance of precipitation,
  and wind speed using the [Darksky API](https://darksky.net/dev).
* Status of two railway operators from National Rail.
* Owned amount and daily change of two cryptocurrencies (Bitcoin and Ethereum).
* 5 news headlines from BBC News in a chosen category.


## Setup

Follow the steps in the
[Waveshare wiki](www.waveshare.com/wiki/7.5inch_e-Paper_HAT) to install the
Python libraries for the 7.5 inch V2 e-paper display.


## Configuration

Copy `config.json.example` and add values appropriate to you:

| Name | Type | Description |
|------|------|-------------|
| `LATITUDE` | String | Latitude |
| `LONGITUDE` | String | Longitude |
| `DARKSKY_KEY` | String | Key for Darksky API |
| `NOMICS_KEY` | String | Key for Nomics crypto ticker API |
| `BTC_AMOUNT` | Float | Amount of Bitcoin owned |
| `ETH_AMOUNT` | Float | Amoutn of Ethereum owned |
| `NEWS_CATEGORY` | String | BBC News category identifier, see below |
| `TWITTER_SCREEN_NAME` | String | Twitter name of an account to show latest tweet. |
| `TWITTER_BEARER_TOKEN` | String | Twitter API Bearer token. |

Available BBC News categories:

* `headlines`
* `world`
* `uk`
* `politics`
* `health`
* `education`
* `science_and_environment`
* `technology`
* `entertainment_and_arts`


## Run

Run with Python 3.x. `crontab` can be used to run on boot.

```shell
python3 main.py
```

When run on a platform other than Raspberry Pi (i.e: not ARM) the display image
is written to `./render.png` instead, which is useful for quickly testing
changes.
