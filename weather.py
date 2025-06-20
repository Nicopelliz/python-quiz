import requests
import datetime
from datetime import datetime
from datetime import timezone
from datetime import timedelta

GIORNI_ITALIANO = [
    "lunedì", "martedì", "mercoledì",
    "giovedì", "venerdì", "sabato", "domenica"
]

def get_weather_forecast(city):
    api_key = "da updatare e nascondere"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=it"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    data = response.json()
    result = []
    used_days = set()
    if data:
        utc_secoffset = data['city']['timezone']
        n_of_hours = utc_secoffset/3600
        check_noon_hour = 12 
        if (n_of_hours % 3 == 1):
            check_noon_hour = 13
        elif (n_of_hours % 3 == 2):
            check_noon_hour = 14
        local_tz = timezone(timedelta(seconds=utc_secoffset))
        for item in data['list']:
            date_txt = item['dt_txt']
            utc_date = datetime.strptime(date_txt, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            local_date = utc_date.astimezone(local_tz).replace(tzinfo=None)
            day = local_date.date()
            if day not in used_days and local_date.hour == check_noon_hour:
                result.append({
                    "day": GIORNI_ITALIANO[local_date.weekday()].capitalize(),
                    "date": local_date.strftime("%d/%m/%Y"),
                    "temp_day": item['main']['temp'],
                    "temp_night": "-",  # Not included in forecast by default
                    "description": item['weather'][0]['description']
                })
                used_days.add(day)

            if len(result) == 3:
                break

    return result
