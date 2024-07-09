import requests
from dotenv import load_dotenv
import os
import datetime as dt

load_dotenv()

HOURS = ["15:00", "17:00", "19:00", "21:00", "23:00"]


def valid_date(date: str) -> None | dt.timedelta:
    """Checks that the date being queried in the weather api is valid.
    The input date cannot be earlier than Jan 1 2010 and cannot be later than 300 days past the current date
    and cannot be between 10 and 14 days past the current date due to an api limitation.

    :parameter date: The date to query. String format YYYY-MM-DD
    Returns timedelta: if the input date is valid the difference between the input date and the current date is returned
    None: if the input date is not in valid format or not within the correct range of acceptable dates"""
    earliest_date = dt.datetime(2010, 1, 1)
    today = dt.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    today_plus_10 = today + dt.timedelta(days=10)
    today_plus_14 = today + dt.timedelta(days=14)
    latest_date = today + dt.timedelta(days=299)
    try:
        dt_date = dt.datetime.strptime(date, "%Y-%m-%d")
        if dt_date < earliest_date or dt_date > latest_date:
            raise InvalidDateError
        if today_plus_10 <= dt_date < today_plus_14:
            raise InvalidDateError
    except InvalidDateError:
        print("Date must be no earlier than Jan 1, 2010 and date cannot be between 10 and 14 days later than current "
              "date and cannot be later than 300 days past the current date")
        return None
    except ValueError:
        print("Date is not in correct format (YYYY-MM-DD)")
        return None
    return dt_date - today


# Converts 24-hour formatted time to 12-hour format
def convert_time(time: str) -> str:
    """Converts a string time in 24-hour format to 12-hour format

    Parameters:
        time: A time string in 24-hour format

    Returns:
        A time string in 12-hour format"""
    am_pm = "AM"
    split_time = time.strip().split(":")
    hour = int(split_time[0])
    minutes = int(split_time[1])
    if hour > 12:
        hour -= 12
        am_pm = "PM"
    return f"{hour}:{minutes:02} {am_pm}"


class WeatherManager:
    """Class designed to interact with the interactive weather api at weatherapi.com"""
    def __init__(self):
        self._key = os.environ.get("WEATHER_API_KEY")

    def get_weather(self, location: str, date: str) -> None | list[dict[str, str]]:
        forcast_call = False
        date_diff = valid_date(date)
        if date_diff is None:
            return None
        if date_diff < dt.timedelta(days=0):
            endpoint_target = "history"
        elif date_diff < dt.timedelta(days=10):
            endpoint_target = "forecast"
            forcast_call = True
        elif date_diff >= dt.timedelta(days=14):
            endpoint_target = "future"
        else:
            return None

        params = {
            "key": self._key,
            "q": location,
            "dt": date,
        }
        endpoint = f"http://api.weatherapi.com/v1/{endpoint_target}.json"

        response = requests.get(url=endpoint, params=params)
        try:
            if response.status_code != 200:
                response.raise_for_status()
        except requests.exceptions.HTTPError:
            print(response.text)
            return None

        weather_data = None
        weather_data_by_hour = []
        if forcast_call:
            for data in response.json()["forecast"]["forecastday"]:
                if data["date"] == date:
                    weather_data = data["hour"]
                    break
        else:
            weather_data = response.json()["forecast"]["forecastday"][0]["hour"]
        for hour_data in weather_data:
            time = hour_data["time"].split()[1]
            if time in HOURS:
                weather_data_by_hour.append({
                    "time": convert_time(time),
                    "condition": hour_data["condition"]["text"].strip(),
                    "cloud_coverage": f"{hour_data['cloud']}%",
                })

        return weather_data_by_hour


class InvalidDateError(ValueError):
    def __init__(self):
        super().__init__()