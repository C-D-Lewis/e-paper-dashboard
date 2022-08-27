# e-paper-dashboard

E-paper photo frame Python app for Waveshare 7.5in V2 e-paper display with
information widgets.

![](photo.jpg)

Included static widgets:

* Time and date
* Current weather - type, temperature, day high/low, chance of precipitation,
  and wind speed using the [Darksky API](https://darksky.net/dev).
* Status of two railway operators from
  [National Rail](http://www.nationalrail.co.uk/service_disruptions/indicator.aspx) (currently hidden).
* Now Playing track with art from Spotify API.
* Owned amount or daily percentage change of two cryptocurrencies (Bitcoin and Ethereum currently)
  from [nomics.com API](https://nomics.com).

Pages of widgets that rotate once a minute:

* 5 news headlines from BBC News in a chosen category.
* Next 5 days weather forecast.
* Latest tweet from a chosen Twitter account.
* One of a number of quotes obtained from
  [https://type.fit/api/quotes](https://type.fit/api/quotes).


## Setup

Follow the steps in the
[Waveshare wiki](www.waveshare.com/wiki/7.5inch_e-Paper_HAT) to install the
required libraries for the 7.5 inch V2 e-paper display.


Install additional Python dependencies:

* `spotipy`
* `PIL`


## Configuration

Copy `config.json.example` and add values appropriate to you:

| Name | Type | Description |
|------|------|-------------|
| `LATITUDE` | String | Local latitude |
| `LONGITUDE` | String | Local longitude |
| `DARKSKY_KEY` | String | Key for Darksky weather API |
| `NOMICS_KEY` | String | Key for Nomics crypto API |
| `BTC_AMOUNT` | Float | Amount of Bitcoin owned |
| `ETH_AMOUNT` | Float | Amoutn of Ethereum owned |
| `NEWS_CATEGORY` | String | BBC News category identifier, from the list below |
| `TWITTER_SCREEN_NAME` | String | Twitter name of an account to show latest tweet |
| `TWITTER_BEARER_TOKEN` | String | Twitter API Bearer token |
| `SPOTIFY_CLIENT_ID` | `String` | Spotify OAuth flow client ID |
| `SPOTIFY_CLIENT_SECRET` | `String` | Spotify OAuth flow client secret |
| `SPOTIFY_REDIRECT_URI` | `String` | Spotify OAuth flow redirect URI |

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

Run with Python 3.x:

```shell
python3 main.py
```

`crontab` can be used to run on boot:

```
@reboot pip3 install spotipy; python3 /home/pi/code/e-paper-dashboard/main.py > /home/pi/e-paper-dashboard.log 2>&1
```

When run on a platform other than Raspberry Pi (i.e: not ARM) the display image
is written to `./render.png` instead, which is useful for quickly testing
changes.
