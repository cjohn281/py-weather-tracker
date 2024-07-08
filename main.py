from weather_manager import WeatherManager
from notification_manager import NotificationManager
import datetime as dt


# Set desired location and future dates (YYYY-mm-dd) to view weather.
# This app was originally designed to plan a trip to Lowell Observatory in
# Flagstaff, AZ in July, so we're going to be looking for rain and clouds on
# the evenings of the dates entered.
location = "Flagstaff"
dates = [
    "2024-07-15",
    "2024-07-20"
]

weather_manager = WeatherManager()
notification_manager = NotificationManager()

message_body = f"WEATHER ALERTS FOR {location}:"
# Gather weather data for each date at the desired location and generate the message body to be sent via text message:
for date in dates:
    weather_data = weather_manager.get_weather(location, date)
    if weather_data is not None:
        dt_date = dt.datetime.strptime(date, "%Y-%m-%d")
        formatted_date = dt_date.strftime("%b %d")
        message_body += f"\n\n{formatted_date}:"
        for hour_data in weather_data:
            pass
            message_body += (f"\n{hour_data['time']}: "
                             f"\n\t\tCondition: {hour_data['condition']} "
                             f"\n\t\tCloud Coverage: {hour_data['cloud_coverage']}")

if message_body != f"WEATHER ALERTS FOR {location}:":
    notification_manager.send_message(message_body)
