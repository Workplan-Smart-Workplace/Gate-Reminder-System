from asyncio.windows_events import NULL
from cgitb import text
from tkinter import *
from pyparsing import condition_as_parse_action
import requests
from PIL import ImageTk, Image
from dotenv import load_dotenv
import os
from io import BytesIO


load_dotenv('weather.env')
WEATHER_API_KEY = os.environ['WEATHER_API_KEY']


def weatherAPICall():
    global weather_image
    city = user_city.get()
    weather_api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + WEATHER_API_KEY
    api_call = requests.get(weather_api).json()
    if (api_call != NULL):
        condition = api_call['weather'][0]['description']
        icon = api_call['weather'][0]['icon']
        city_name = api_call['name']
        print(city_name)
        temp = int(api_call['main']['temp'] - 273.15)
        wind_speed = api_call['wind']['speed']
        city_info.config(text=city_name)
        temp_info.config(text=str(temp)+ chr(176) + "Celsius")
        weather_status.config(text=condition)
        wind.config(text= "The Wind Speed is: " + str(wind_speed) + " Km/h")
        print(condition)
        icon_url = "http://openweathermap.org/img/wn/" + icon + "@2x.png"
        image_icon = requests.get(icon_url)
        weather_photo = Image.open(BytesIO(image_icon.content))
        weather_photo = weather_photo.resize((150,150))
        weather_photo = ImageTk.PhotoImage(weather_photo)
        weather_pic.config(image=weather_photo)
        weather_pic.photo_ref = weather_photo
        if "rain" in condition:
            status.config(text="Don't forget your umbrella!")
        elif "freezing" in condition:
            status.config(text="It's slippery outside, bundle up and watch for ice!")
        elif "snow" in condition:
            status.config(text="It's slippery outside, bundle up and watch for ice!")
        elif "mist" in condition:
            status.config(text="Low Visibility, Drive Safe!")
        elif "overcast clouds" in condition:
            status.config(text= "There is cloud cover, bundle up!")
        else:
            status.config(text="Normal weather conditions, nothing to be concerned about.")
        
main = Tk()
main.geometry("1280x720")
main.title("Daily Weather")
main.config(background="light blue")
user_city = StringVar()
weather_image = Image.open("1530391_weather_clouds_sun_sunny_icon.png")
weather_image = weather_image.resize((150,150))
weather_image = ImageTk.PhotoImage(weather_image)

user_prompt = Label(main, font=("Cascadia Code SemiBold", 20), text="Enter Your City.").pack()
city_entry = Entry(main, background="grey", textvariable=user_city).pack()
Button(main, text='Enter', background='grey',command=weatherAPICall).pack()

city_info = Label(main, font=("Cascadia Code SemiBold", 20), background="light blue")
city_info.pack()
temp_info = Label(main, font=("Cascadia Code SemiBold", 50), background="light blue")
temp_info.pack()
weather_pic = Label(main, image=weather_image, background="light blue")
weather_pic.pack()
weather_status = Label(main, font=("Cascadia Code SemiBold", 20), background="light blue")
weather_status.pack()
wind = Label(main, font=("Cascadia Code SemiBold", 20), background="light blue")
wind.pack()
status = Label(main, font=("Cascadia Code SemiBold", 20), background="light blue")
status.pack()
main.mainloop()