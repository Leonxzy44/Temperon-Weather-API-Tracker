import urllib.request
import json
import datetime
import csv
from urllib.parse import urlencode
import time

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


banner = f"""
{Colors.BLUE}{Colors.BOLD}
                                                     
▄▄▄▄▄▄▄▄▄                                           
▀▀▀███▀▀▀                                           
   ███ ▄█▀█▄ ███▄███▄ ████▄ ▄█▀█▄ ████▄ ▄███▄ ████▄ 
   ███ ██▄█▀ ██ ██ ██ ██ ██ ██▄█▀ ██ ▀▀ ██ ██ ██ ██ 
   ███ ▀█▄▄▄ ██ ██ ██ ████▀ ▀█▄▄▄ ██    ▀███▀ ██ ██ 
                      ██                            
                      ▀▀                            
{Colors.END}
"""

print(banner)
print(f"{Colors.GREEN}Welcome to Temperon!{Colors.END}")
print(f"{Colors.BLUE}This program will fetch temperatures for the past week and save them to a CSV file.{Colors.END}")
print(f"{Colors.BLUE}Open the CSV in Excel to view and sort the data.{Colors.END}\n")

API_KEY = "fbd99b8db3d0426f876143132251612"
city = input(f"{Colors.GREEN}Enter the name of your town/city: {Colors.END}").strip()

data = []
today = datetime.date.today()

def c_to_f(c: float) -> float:
    return (c * 9.0 / 5.0) + 32.0

for i in range(7, 0, -1):
    day = today - datetime.timedelta(days=i)

    params = urlencode({"key": API_KEY, "q": city, "dt": str(day)})
    url = f"http://api.weatherapi.com/v1/history.json?{params}"

    try:
        with urllib.request.urlopen(url) as response:
            weather_data = json.loads(response.read())
            forecast_day = weather_data["forecast"]["forecastday"][0]["day"]

            max_c = float(forecast_day["maxtemp_c"])
            min_c = float(forecast_day["mintemp_c"])
            avg_c = float(forecast_day["avgtemp_c"])

            row = {
                "City": city,
                "Date": str(day),
                "Day": day.strftime("%A"),
                "Max Temp C": round(max_c, 1),
                "Min Temp C": round(min_c, 1),
                "Avg Temp C": round(avg_c, 1),
                "Max Temp F": round(c_to_f(max_c), 1),
                "Min Temp F": round(c_to_f(min_c), 1),
                "Avg Temp F": round(c_to_f(avg_c), 1),
                "Total Precip mm": round(float(forecast_day.get("totalprecip_mm", 0.0)), 1),
                "Avg Humidity %": int(round(float(forecast_day.get("avghumidity", 0.0)))),
                "Max Wind kph": round(float(forecast_day.get("maxwind_kph", 0.0)), 1),
                "Condition": forecast_day.get("condition", {}).get("text", "")
            }
            data.append(row)

            print(f"{Colors.BLUE}Fetched data for {day}{Colors.END}")

    except Exception as e:
        print(f"{Colors.FAIL}Error fetching data for {day}: {e}{Colors.END}")
        print(f"{Colors.WARNING}Check your API key and the city name (try adding country/state if needed).{Colors.END}")
        break

if data:
    safe_city = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in city).strip("_")
    filename = f"weather_{safe_city}_{today}.csv"

    fieldnames = [
        "City", "Date", "Day",
        "Max Temp C", "Min Temp C", "Avg Temp C",
        "Max Temp F", "Min Temp F", "Avg Temp F",
        "Total Precip mm", "Avg Humidity %", "Max Wind kph",
        "Condition"
    ]

    
    with open(filename, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"\n{Colors.GREEN}📥 Data saved to {filename}!{Colors.END}")
    print(f"{Colors.BLUE}👉 Tip: In Excel, select row 1 → Home → Format as Table.{Colors.END}")
    print("Copy & paste the link to your searchbar to visit the xsls file!")
else:
    print(f"{Colors.FAIL}No data fetched. Please check your input and API key.{Colors.END}")




time.sleep(5000)