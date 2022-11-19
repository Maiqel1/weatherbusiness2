# Utility functions

from typing import List, Union

import geocoder
import requests
from decouple import config
from fastapi import HTTPException, status
import datetime


def geocode_address(
    city_name: str, lga: str = "", state: str = ""
) -> Union[List[str], None]:
    """Get geocode of city, lga and state

    :param city_name: city name
    :type city_name: str
    :param lga: local government area
    :type lga: str or None
    :param state: state
    :type state: str or None
    :return: geocode in format [lat, long]
    :rtype: list or None
    """

    address = f"{city_name}"

    if lga:
        address += f", {lga}"
    if state:
        address += f", {state}"

    g = geocoder.osm(address)
    return g.latlng


# function to call the open weather api and fetch the required data
# Required data = "lon" and "lat"
def weather_api_call(lon, lat, *args, **kwargs):

    API_key = config("API_KEY")

    # converts given parameters into required types
    lon = float(lon)
    lat = float(lat)

    # Call API and converts response into dictionary
    open_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}"

    try:
        response = requests.get(open_weather_url).json()

        # Error messages for unknown city or street names or invalid API key
        if response.status_code != 200:
            return f"Can't retrive weather data for this location"

        weather_conditions = response['weather'] #returns a lists

        for detail in weather_conditions:
            current_weather = detail['main']
            weather_description = detail['description']

        return {
            "current_weather": current_weather,
            "weather_description": weather_description
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Weather conditon not found.Please retry again"
        )

def immediate_weather_api_call(lng, lat, *args, **kwargs):

    API_key = config("API_KEY")

    # converts given parameters into required types
    lng = float(lng)
    lat = float(lat)

    # Call API and converts response into dictionary
    open_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={API_key}"

    try:
        response = requests.get(open_weather_url).json()

        # Error messages for unknown city or street names or invalid API key
        if response.status_code != 200:
            return f"Can't retrive weather data for this location"
        
        weather_conditions = response['list'] #returns a lists

        time_epoch = weather_conditions[0]['dt']
        main = weather_conditions[0]['weather'][0]['main']
        description = weather_conditions[0]['weather'][0]['description']

        time_format = datetime.datetime.fromtimestamp(time_epoch)
        date = time_format.strftime('%d %B, %Y')
        am_or_pm = time_format.strftime('%p')
        hour_minute = time_format.strftime('%I:%M')
        time_output = f"{hour_minute}{am_or_pm.lower()}"
        
        return {
            "main": main,
            "description": description,
            "date": date,
            "time": time_output
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= f"Weather conditon not found.Please retry again"
        )
