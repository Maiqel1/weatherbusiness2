from app.utils import get_weather_forecast, convert_epoch_to_datetime
import pytest


def test_convert_epoch_to_datetime():
    epoch_time = 1612904800
    expected = {
        "date": "09 Feb, 2021",
        "time": "10:06pm"
    }
    print(convert_epoch_to_datetime(epoch_time))
    assert convert_epoch_to_datetime(epoch_time) == expected


class TestGetWeatherForecast:
    def test_weather_forcasts_valid(self, mocker):
        """Test weather forecast endpoint"""
        # mocker request.get json response
        mocker.patch(
            'requests.get',
            return_value=mocker.Mock(
                status_code=200,
                json=mocker.Mock(
                    return_value={
                        "cod": "200",
                        "message": 0,
                        "cnt": 40,
                        "list": [
                            {
                                "test": "demo"
                            },
                        ]
                    }
                )
            )
        )

        results = get_weather_forecast(6.5244, 3.3792)
        assert results == [{"test": "demo"}]

    @pytest.mark.parametrize(
        "cod",
        [
            "400",
            "401",
        ]
    )
    def test_weather_forcasts_invalid(self, cod, mocker):
        """Test weather forecast endpoint"""
        # mocker request.get json response
        mocker.patch(
            'requests.get',
            return_value=mocker.Mock(
                status_code=200,
                json=mocker.Mock(
                    return_value={
                        "cod": cod,
                        "message": 0,
                        "cnt": 40,
                        "list": [
                            {
                                "test": "demo"
                            },
                        ]
                    }
                )
            )
        )

        with pytest.raises(Exception):
            get_weather_forecast(6.5244, 3.3792)

    def test_weather_forcasts_error(self, mocker):
        """Test weather forecast endpoint"""
        mocker.patch(
            'requests.get',
            return_value=mocker.Mock(
                status_code=400
            )
        )

        with pytest.raises(Exception):
            get_weather_forecast(6.5244, 3.3792)
