# FastApi imports
from typing import List

from app.models import SingleWeatherResponse
from fastapi import APIRouter
from fastapi import HTTPException, status
# Internal import
from app.schemas import *  # noqa: F401, F403
from app.client import weather
from app.utils import (
    get_weather_forecast,
    convert_epoch_to_datetime,
    get_immediate_weather_api_call, convert)


router = APIRouter(
    prefix="/weather",
    tags=['weather']
)


@router.get('/forecasts', response_model=List[SingleWeatherResponse])
async def weather_forcasts(lat: float, lon: float):
    """Get weather forecast for next 10 steps"""
    try:
        weather_forecasts_data = get_weather_forecast(lat, lon)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't retrive weather data for this location"
        )

    results = []

    for forcast in weather_forecasts_data:
        data = convert_epoch_to_datetime(forcast.get('dt'))
        data['main'] = forcast['weather'][0]['main']
        data['description'] = forcast['weather'][0]['description']
        results.append(data)

    return results

@router.get("/forecasts/immediate")
async def immediate_weather_forecast(lat: float=None, lng: float=None):

    if lat is None and lng is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"invalid longitute and latitude"
        )
    result = get_immediate_weather_api_call(lat, lng)

    return result


@router.get("/forecasts/tomorrow")
async def weather_data(lat: float, lon: float):
    try:
        result = weather(lat, lon)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't retrive weather data for this location"
        )

    epoch = convert()

    starting_point = None

    # print(result)
    for index, _data in enumerate(result):
        if _data['dt'] >= epoch:
            starting_point = index
            break

    if starting_point is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = f"Weather condition not found, Please try again"
        )
    result = result[starting_point:10]
    bus = []
    for forecast in result:
        data = convert_epoch_to_datetime(forecast.get('dt'))
        data['main'] = forecast['weather'][0]['main']
        data['description'] = forecast['weather'][0]['description']
        bus.append(data)
    return bus
