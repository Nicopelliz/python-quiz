import requests
import datetime
from datetime import datetime
from datetime import timezone
from datetime import timedelta
import os
from dotenv import load_dotenv

# Necessario solo localmente
load_dotenv()
api_key = os.getenv("API_KEY")

GIORNI_ITALIANO = [
    "lunedì", "martedì", "mercoledì",
    "giovedì", "venerdì", "sabato", "domenica"
]


def get_weather_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=it"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    data = response.json()
    result = []
    used_days = set()
    temp_noon = None
    temp_midnight = None
    if data:
        utc_secoffset = data['city']['timezone']
        n_of_hours = utc_secoffset/3600
        check_noon_hour = 12 
        check_midnight_hour = 0
        if (n_of_hours % 3 == 1):
            check_noon_hour = 13
            check_midnight_hour = 1
        elif (n_of_hours % 3 == 2):
            check_noon_hour = 14
            check_midnight_hour = 2
        local_tz = timezone(timedelta(seconds=utc_secoffset))
        # Il modo in cui ho fatto l'algoritmo suppone che i 
        # dati arrivino sempre in ordine
        for item in data['list']:
            date_txt = item['dt_txt']
            utc_date = datetime.strptime(date_txt, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            local_date = utc_date.astimezone(local_tz).replace(tzinfo=None)
            day = local_date.date()
            if local_date.hour == check_noon_hour:
                temp_noon = item['main']['temp']
            if local_date.hour == check_midnight_hour:
                temp_midnight = item['main']['temp']
            if temp_noon is not None and temp_midnight is not None and day not in used_days:
                result.append({
                    "day": GIORNI_ITALIANO[local_date.weekday()].capitalize(),
                    "date": local_date.strftime("%d/%m/%Y"),
                    "temp_day": temp_noon,
                    "temp_night": temp_midnight,
                })
                used_days.add(day)
                temp_noon = None
                temp_midnight = None

            if len(result) == 3:
                break
    return result
