import json
import logging
import urllib.error
import urllib.request
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Config:
    KEYSTONE_LAT: float = 39.6
    KEYSTONE_LON: float = -105.93
    NWS_USER_AGENT: str = "SnowWeatherAlert/1.0"
    FORECAST_PERIODS_TO_CHECK: int = 3
    SNOW_KEYWORDS: tuple[str, ...] = ("snow", "flurries", "wintry mix", "winter weather", "blizzard")


@dataclass
class SnowPeriod:
    name: str
    forecast: str
    details: str

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "forecast": self.forecast, "details": self.details}


class WeatherService:
    def __init__(self, config: Config):
        self.config = config

    def _make_request(self, url: str) -> dict:
        headers = {"User-Agent": self.config.NWS_USER_AGENT}
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=10) as response:
            data: dict = json.loads(response.read().decode())
            return data

    def get_forecast(self) -> list[dict] | None:
        try:
            points_url = (
                f"https://api.weather.gov/points/"
                f"{self.config.KEYSTONE_LAT},{self.config.KEYSTONE_LON}"
            )
            logger.info(f"Fetching points data from: {points_url}")
            points_data = self._make_request(points_url)

            forecast_url = points_data["properties"]["forecast"]
            logger.info(f"Fetching forecast from: {forecast_url}")
            forecast_data = self._make_request(forecast_url)

            periods: list[dict] = forecast_data["properties"]["periods"]
            logger.info(f"Successfully fetched {len(periods)} forecast periods")
            return periods

        except urllib.error.HTTPError as e:
            logger.error(f"HTTP error fetching weather data: {e.code} - {e.reason}")
            return None
        except urllib.error.URLError as e:
            logger.error(f"URL error fetching weather data: {e.reason}")
            return None
        except KeyError as e:
            logger.error(f"Unexpected API response structure: missing key {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching weather data: {e}")
            return None


class SnowDetector:
    def __init__(self, config: Config):
        self.config = config

    def check_for_snow(self, forecast_periods: list[dict]) -> tuple[bool, list[SnowPeriod]]:
        if not forecast_periods:
            logger.warning("No forecast periods provided")
            return False, []

        snow_periods: list[SnowPeriod] = []

        periods_to_check = forecast_periods[: self.config.FORECAST_PERIODS_TO_CHECK]
        logger.info(f"Checking {len(periods_to_check)} forecast periods for snow")

        for period in periods_to_check:
            try:
                forecast_text = period["detailedForecast"].lower()
                short_forecast = period["shortForecast"].lower()

                if any(
                    keyword in forecast_text or keyword in short_forecast
                    for keyword in self.config.SNOW_KEYWORDS
                ):
                    snow_period = SnowPeriod(
                        name=period["name"],
                        forecast=period["shortForecast"],
                        details=period["detailedForecast"],
                    )
                    snow_periods.append(snow_period)
                    logger.info(f"Snow detected in period: {period['name']}")

            except KeyError as e:
                logger.warning(f"Missing key in forecast period: {e}")
                continue

        has_snow = len(snow_periods) > 0
        logger.info(f"Snow detection complete: {has_snow} ({len(snow_periods)} periods)")
        return has_snow, snow_periods


def check_snow_forecast(config: Config) -> tuple[bool, list[SnowPeriod]]:
    weather_service = WeatherService(config)
    snow_detector = SnowDetector(config)

    forecast_periods = weather_service.get_forecast()
    if not forecast_periods:
        return False, []

    return snow_detector.check_for_snow(forecast_periods)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = Config()
    has_snow, snow_periods = check_snow_forecast(config)

    print(f"\nSnow detected: {has_snow}")
    if snow_periods:
        print("\nSnow periods:")
        for period in snow_periods:
            print(f"  - {period.name}: {period.forecast}")
