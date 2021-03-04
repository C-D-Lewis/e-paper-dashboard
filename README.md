# e-paper-frame

E-paper photo frame Python for Waveshare 7.5in V2 e-paper display with
information widgets.


## Setup

Follow the steps in the Waveshare wiki to install the Python libraries for the
7.5 inch V2 e-paper display.


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


## Run on startup

```shell
python3 main.py
```

`crontab` could be used to run on boot.
