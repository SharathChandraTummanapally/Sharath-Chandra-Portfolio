# DSC 510
# Week 10
# Program for forecasting weather information based on the user input.
# Programming Assignment Week 10
# Author Sharath Chandra Tummanapally
# 8/13/2021


import json
import requests
from geopy.geocoders import Nominatim


def get_state_code(lat, long):
    """Function to get state code by using geopy library."""

    state_code = ''
    state_name = ''
    lat_long = lat + ',' + long

    try:
        # Getting location details from geopy by passing the latitude and longitude.
        geo_locator = Nominatim(user_agent="geoapiExercises")
        location = geo_locator.geocode(lat_long, addressdetails=True)
    except:
        return state_code

    else:
        # Setting the state name from location object.
        if bool(location):
            state_name = location.raw['address']['state']
        if bool(state_name):
            with open('StatesAndAbv.json') as f:
                states_and_abv = json.load(f)
                # Checking the state name in json file to get the state code.
                for abv, state in states_and_abv.items():
                    if state.lower() == state_name.strip().lower():
                        state_code = abv
                        break

    return state_code.upper()


def convert_temp(temps, temp_type):
    """Function to Convert temperature in Kelvin to Celsius/Fahrenheit"""

    converted_temp_lst = []
    for item in temps:
        if temp_type == 'C':
            item = item - 273.15
        elif temp_type == 'F':
            item = (item - 273.15) * 9/5 + 32
        converted_temp_lst.append(str(round(item,1)))
    return converted_temp_lst


def weather_forecast(frame, city_name, state_abv, zip_code, temp_type):
    """Function to call weather API and return weather data"""

    api_key = 'f8a23b037f0467859d5cc63b1781e18d'
    err_msg = ''
    user_note = ''
    weather_data = {}

    # Setting the URL based on user selection.
    if frame == 'cityBtnFrame':
        url = 'https://api.openweathermap.org/data/2.5/weather?q={cityName},{stateCode},us&appid={apiKey}'
    else:
        url = 'https://api.openweathermap.org/data/2.5/weather?zip={zipcode},us&appid={apiKey}'

    try:
        # Requesting the Open Weather API for weather data based on City/ZipCode.
        response = requests.get(url.format(cityName=city_name, stateCode=state_abv, zipcode=zip_code, apiKey=api_key))
        response.raise_for_status()
        # Storing the JSON object data from API.
        data = response.json()

    except requests.exceptions.ConnectionError:  # Raises this exception, if connection is failed.
        err_msg = 'Connection failed while attempting to request the data!'
    except requests.exceptions.HTTPError:  # Raises this exception, if no data is returned.
        err_msg = 'Error : ' + str(json.loads(response.text)['message']).capitalize() + '!' if frame == 'cityBtnFrame' else 'Error : Invalid Zip Code!'
    except Exception as e:  # Raises this exception, if other error occurred.
        err_msg = 'Error : ' + str(e)

    else:
        # Setting the weather data from JSON object.
        if bool(data):
            city_name = data['name']
            temp_dict = data['main']
            cloud_cover = data['weather'][0]['description']
            latitude = str(data['coord']['lat'])
            longitude = str(data['coord']['lon'])
            temp_lst = [temp_dict['temp'], temp_dict['temp_max'], temp_dict['temp_min']]

            # Getting the state code by latitude and longitude.
            state_code = get_state_code(latitude, longitude)
            if bool(state_abv) and state_abv.lower() != state_code.lower():
                user_note = '** You have given the invalid state code, thus displaying the weather conditions of default state code of current city.'

            # Calling function to convert the temperatures from K to C/F based on user selection.
            if temp_type.upper() != 'K':
                converted_temp_lst = convert_temp(temp_lst, temp_type.upper())
            else:
                converted_temp_lst = temp_lst

            # Creating a weather dictionary object to display the data to user.
            weather_data = {'City Name': city_name.capitalize() + ', ' + state_code,
                            'Current Temperature': str(converted_temp_lst[0]) + ' degrees',
                            'High Temperature': str(converted_temp_lst[1]) + ' degrees',
                            'Low Temperature': str(converted_temp_lst[2]) + ' degrees',
                            'Pressure': str(temp_dict['pressure']) + ' hPa',
                            'Humidity': str(temp_dict['humidity']) + ' %',
                            'Cloud Cover': cloud_cover.capitalize()
                            }

    return weather_data, err_msg, user_note



