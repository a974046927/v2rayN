from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class WeatherSummary:
    kind: str
    temperature: float | None
    pet_line: str
    location: str = ""
    source: str = ""


RAIN_CODES = {
    51,
    53,
    55,
    56,
    57,
    61,
    63,
    65,
    66,
    67,
    80,
    81,
    82,
    95,
    96,
    99,
}


def summarize_weather(data: dict[str, Any]) -> WeatherSummary:
    code = int(data.get("weather_code", data.get("weathercode", -1)))
    precipitation = float(data.get("precipitation", 0) or 0)
    temperature = data.get("temperature")
    if temperature is not None:
        temperature = float(temperature)
    location = str(data.get("location", "") or "")
    source = str(data.get("source", "") or "")

    if precipitation > 0.2 or code in RAIN_CODES:
        place = f"{location} " if location else ""
        return WeatherSummary("rain", temperature, f"{place}外面有雨，哥哥，出门记得带伞。", location, source)
    if code in {0, 1} and precipitation <= 0.1:
        place = f"{location} " if location else ""
        return WeatherSummary("sunny", temperature, f"{place}今天太阳不错，哥哥，适合起来走一走。", location, source)
    place = f"{location} " if location else ""
    return WeatherSummary("cloudy", temperature, f"{place}天气有点普通，但我还是会提醒你休息。", location, source)


def _read_json(url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "yoruame-pet/0.1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def locate_by_ip(timeout: int) -> tuple[float, float, str]:
    data = _read_json("https://ipapi.co/json/", timeout)
    return float(data["latitude"]), float(data["longitude"]), str(data.get("city", ""))


def geocode_city(city: str, timeout: int) -> tuple[float, float, str] | None:
    query = urllib.parse.urlencode({"name": city, "count": 1, "language": "zh"})
    data = _read_json(f"https://geocoding-api.open-meteo.com/v1/search?{query}", timeout)
    results = data.get("results") or []
    if not results:
        return None
    first = results[0]
    return float(first["latitude"]), float(first["longitude"]), str(first.get("name", city))


def fetch_weather_summary(config: dict[str, Any]) -> WeatherSummary | None:
    timeout = int(config.get("request_timeout_seconds", 6))
    city = str(config.get("weather_city", "")).strip()
    try:
        if city:
            location = geocode_city(city, timeout)
            if location is None:
                return None
            latitude, longitude, resolved_name = location
            source = "configured_city"
        else:
            latitude, longitude, resolved_name = locate_by_ip(timeout)
            source = "ip"
        query = urllib.parse.urlencode(
            {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,precipitation,weather_code",
            }
        )
        data = _read_json(f"https://api.open-meteo.com/v1/forecast?{query}", timeout)
        current = data.get("current") or {}
        return summarize_weather(
            {
                "weather_code": current.get("weather_code"),
                "precipitation": current.get("precipitation", 0),
                "temperature": current.get("temperature_2m"),
                "location": resolved_name,
                "source": source,
            }
        )
    except Exception:
        return None
