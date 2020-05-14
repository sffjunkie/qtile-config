"""OpenWeatherMap widget for QTile"""

import time

import requests

from libqtile import pangocffi
from libqtile.log_utils import logger
from libqtile.widget import base

ICON_FONT = "Weather Icons"

if ICON_FONT == "Weather Icons":
    ICONS = {
        "01d": "\uF00D",  # Clear sky
        "01n": "\uF02E",
        "02d": "\uF002",  # Few clouds
        "02n": "\uF086",
        "03d": "\uF041",  # Scattered Clouds
        "03n": "\uF041",
        "04d": "\uF013",  # Broken clouds
        "04n": "\uF013",
        "09d": "\uF009",  # Shower Rain
        "09n": "\uF037",
        "10d": "\uF008",  # Rain
        "10n": "\uF036",
        "11d": "\uF010",  # Thunderstorm
        "11n": "\uF03B",
        "13d": "\uF00A",  # Snow
        "13n": "\uF038",
        "50d": "\uF003",  # Mist
        "50n": "\uF04A",
        "sleetd": "\uF0B2",
        "sleetn": "\uF0B3",
    }
elif ICON_FONT == "Material Design Icons":
    ICONS = {
        "01d": "\U000F0599",  # Clear sky
        "01n": "\U000F0594",
        "02d": "\U000F0595",  # Few clouds
        "02n": "\U000F0F31",
        "03d": "\U000F0595",  # Scattered Clouds
        "03n": "\U000F0F31",
        "04d": "\U000F0590",  # Broken clouds
        "04n": "\U000F0F31",
        "09d": "\U000F0F33",  # Shower Rain
        "09n": "\U000F0F33",
        "10d": "\U000F0597",  # Rain
        "10n": "\U000F0597",
        "11d": "\U000F0596",  # Thunderstorm
        "11n": "\U000F0596",
        "13d": "\U000F0598",  # Snow
        "13n": "\U000F0598",
        "50d": "\U000F0591",  # Mist
        "50n": "\U000F0591",
        "sleetd": "\U000F0596",
        "sleetn": "\U000F0596",
    }

CONDITION_CODES = {
    200: ("thunderstorm with light rain", ICONS["11d"], ICONS["11n"]),
    201: ("thunderstorm with rain", ICONS["11d"], ICONS["11n"]),
    202: ("thunderstorm with heavy rain", ICONS["11d"], ICONS["11n"]),
    210: ("light thunderstorm", ICONS["11d"], ICONS["11n"]),
    211: ("thunderstorm", ICONS["11d"], ICONS["11n"]),
    212: ("heavy thunderstorm", ICONS["11d"], ICONS["11n"]),
    221: ("ragged thunderstorm", ICONS["11d"], ICONS["11n"]),
    230: ("thunderstorm with light drizzle", ICONS["11d"], ICONS["11n"]),
    231: ("thunderstorm with drizzle", ICONS["11d"], ICONS["11n"]),
    232: ("thunderstorm with heavy drizzle", ICONS["11d"], ICONS["11n"]),
    300: ("light intensity drizzle", ICONS["09d"], ICONS["09n"]),
    301: ("drizzle", ICONS["09d"], ICONS["09n"]),
    302: ("heavy intensity drizzle", ICONS["09d"], ICONS["09n"]),
    310: ("light intensity drizzle rain", ICONS["09d"], ICONS["09n"]),
    311: ("drizzle rain", ICONS["09d"], ICONS["09n"]),
    312: ("heavy intensity drizzle rain", ICONS["09d"], ICONS["09n"]),
    313: ("shower rain and drizzle", ICONS["09d"], ICONS["09n"]),
    314: ("heavy shower rain and drizle", ICONS["09d"], ICONS["09n"]),
    321: ("shower drizzle", ICONS["09d"], ICONS["09n"]),
    500: ("light rain", ICONS["10d"], ICONS["10n"]),
    501: ("moderatelight rain", ICONS["10d"], ICONS["10n"]),
    502: ("heavy intensity rain", ICONS["10d"], ICONS["10n"]),
    503: ("very heavy rain", ICONS["10d"], ICONS["10n"]),
    504: ("extreme rain", ICONS["10d"], ICONS["10n"]),
    511: ("freezing rain", ICONS["13d"], ICONS["13n"]),
    520: ("light intensity shower rain", ICONS["09d"], ICONS["09n"]),
    521: ("shower rain", ICONS["09d"], ICONS["09n"]),
    522: ("heavy intensity shower rain", ICONS["09d"], ICONS["09n"]),
    531: ("ragged shower rain", ICONS["09d"], ICONS["09n"]),
    600: ("light snow", ICONS["13d"], ICONS["13n"]),
    601: ("snow", ICONS["13d"], ICONS["13n"]),
    602: ("heavy snow", ICONS["13d"], ICONS["13n"]),
    611: ("sleet", "sleetd", "sleetn"),
    612: ("light shower sleet", ICONS["13d"], ICONS["13n"]),
    613: ("shower sleet", ICONS["13d"], ICONS["13n"]),
    615: ("light rain and snow", ICONS["13d"], ICONS["13n"]),
    616: ("rain and snow", ICONS["13d"], ICONS["13n"]),
    620: ("light shower snow", ICONS["13d"], ICONS["13n"]),
    621: ("shower snow", ICONS["13d"], ICONS["13n"]),
    622: ("heavy shower snow", ICONS["13d"], ICONS["13n"]),
    701: ("mist", ICONS["50d"], ICONS["50n"]),
    711: ("smoke", ICONS["50d"], ICONS["50n"]),
    721: ("haze", ICONS["50d"], ICONS["50n"]),
    731: ("sand / dust swirls", ICONS["50d"], ICONS["50n"]),
    741: ("fog", ICONS["50d"], ICONS["50n"]),
    751: ("sand", ICONS["50d"], ICONS["50n"]),
    761: ("dust", ICONS["50d"], ICONS["50n"]),
    762: ("volcanic ash", ICONS["50d"], ICONS["50n"]),
    771: ("squalls", ICONS["50d"], ICONS["50n"]),
    781: ("tornado", ICONS["50d"], ICONS["50n"]),
    800: ("clear sky", ICONS["01d"], ICONS["01n"]),
    801: ("few clouds", ICONS["02d"], ICONS["02n"]),
    802: ("scattered clouds", ICONS["03d"], ICONS["03n"]),
    803: ("broken clouds", ICONS["04d"], ICONS["04d"]),
    804: ("overcast clouds", ICONS["04d"], ICONS["04d"]),
}


class OpenWeatherMap(base.ThreadedPollText):
    """OpenWeatherMap widget for QTile"""

    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("apikey", "", "API Key for OpenWeatherMap data"),
        ("font", "Weather Icons", "Font to use for weather icons"),
        (
            "format",
            '{temp:.1f}{temp_units} <span face="{icon_font}">{icon}</span>',
            "Format string",
        ),
        ("update_interval", 3600, "Update interval in seconds between look ups"),
        ("latitude", 51.4934, "Latitude to look up weather data for"),
        ("longitude", 0.0098, "Longitude to look up weather data for"),
        ("units", "metric", "Temperature units to use"),
    ]

    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(OpenWeatherMap.defaults)
        if not self.apikey:
            logger.exception("OpenWeatherMap: An API key is required.")
        self.url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&appid={self.apikey}&units={self.units}"

    def _configure(self, qtile, bar) -> None:
        self.markup = True
        base._TextBox._configure(self, qtile, bar)

    def update(self, text):
        """Update the text box."""
        old_width = self.layout.width
        if self.status != 200:
            return
        self.text = text

        if self.layout.width == old_width:
            self.draw()
        else:
            self.bar.draw()

    def poll(self):
        resp = requests.get(self.url)
        self.status = resp.status_code
        if resp.status_code == 200:
            _lookup = lambda group, key: group[key] if key in group else ""
            data = resp.json()
            owm_icon = _lookup(data["weather"][0], "icon")
            day = owm_icon[-1] == "d"

            owm_condition = _lookup(data["weather"][0], "id")
            if owm_condition in CONDITION_CODES:
                condition = CONDITION_CODES[owm_condition][0].capitalize()
                if day:
                    icon = CONDITION_CODES[owm_condition][1]
                else:
                    icon = CONDITION_CODES[owm_condition][2]
            else:
                condition = "Unknown"
                logger.warning(
                    f"OpenWeatherMap: Unknown condition {owm_condition} received"
                )
                if day:
                    icon = ICONS["01d"]
                else:
                    icon = ICONS["01n"]

            info = {
                "icon": icon,
                "icon_font": ICON_FONT,
                "condition": condition,
                "temp_units": "°C" if self.units == "metric" else "°F",
                "temp": _lookup(data["main"], "temp"),
                "temp_min": _lookup(data["main"], "temp_min"),
                "temp_max": _lookup(data["main"], "temp_max"),
                "temp_feels_like": _lookup(data["main"], "feels_like"),
                "pressure": _lookup(data["main"], "pressure"),
                "humidity": _lookup(data["main"], "humidity"),
            }

            return self.format.format(**info)
        else:
            return f"OpenWeatherMap Error {resp.status_code}"
