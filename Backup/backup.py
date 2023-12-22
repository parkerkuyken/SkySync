
import customtkinter as ck
from datetime import date
import datetime as dt
from PIL import Image, ImageTk
import requests

api_key = "77ba6be4d7ba2a4d547c099a7efff889"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

CITY = None  # Initialize CITY variable
response = None  # Initialize response variable









def kelvin_to_Fahrenheit_Celsius(kelvin):
    Celsius = kelvin - 273.15
    Fahrenheit = Celsius * 9/5 + 32
    return Fahrenheit, Celsius

def update_weather_labels():
    global CITY, response
    url = base_url + "appid=" + api_key + "&q=" + CITY
    try:
        response = requests.get(url).json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        response = None

def get_city(event=None):
    global CITY
    CITY = city_entry.get()
    # Make sure CITY is not an empty string before updating labels
    if CITY:
        update_weather_labels()
        # Update GUI labels with the new weather information
        update_gui_labels()
        city_country = response["sys"]["country"]
        selected_city.configure(text=f"{CITY.title()}, {city_country}")

def get_wind_direction(degree):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(degree/45) % 8
    return directions[index]

def convert_to_standard_time(time_24hr):
            hours, minutes = map(int, time_24hr.split(':'))
            period = 'am' if hours < 12 else 'pm'
            if hours == 0:
                hours = 12
            elif hours > 12:
                hours -= 12
            standard_time = f"{hours}:{minutes:02d} {period}"
            return standard_time






def update_gui_labels():
    global response
    if response and "main" in response:
        # CURRENTLY TAB ===============================================================================

        temp_kelvin = response["main"]["temp"]
        temp_fahrenheit = kelvin_to_Fahrenheit_Celsius(temp_kelvin)
        temp_fahrenheit = tuple(round(value) for value in temp_fahrenheit)
        current_temp.configure(text=f"{temp_fahrenheit[0]} °F")

        high_kelvin = response["main"]["temp_max"]
        high_fahrenheit = kelvin_to_Fahrenheit_Celsius(high_kelvin)
        high_fahrenheit = tuple(round(value) for value in high_fahrenheit)
        temp_max.configure(text=f"High {high_fahrenheit[0]} °F")

        # Low
        low_kelvin = response["main"]["temp_min"]
        low_fahrenheit = kelvin_to_Fahrenheit_Celsius(low_kelvin)
        low_fahrenheit = tuple(round(value) for value in low_fahrenheit)
        temp_min.configure(text=f"Low {low_fahrenheit[0]} °F")

        # Coords
        longitude = str(response["coord"]["lon"]) + " , " + str(response["coord"]["lat"])
        city_long.configure(text=f"{longitude}")

        # Time
        today = date.today()
        day = today.strftime("%B %d, %Y")
        current_date.configure(text=f"{day}")

        # Icons
        if "weather" in response and response["weather"]:
            icon_code = response["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/w/{icon_code}.png"

            try:
                scale_factor = 2.7  # You can adjust this factor
                icon_image = Image.open(requests.get(icon_url, stream=True).raw)
                icon_image = icon_image.resize((int(icon_image.width * scale_factor), int(icon_image.height * scale_factor)))
                icon_photo = ImageTk.PhotoImage(icon_image)
                weather_icon.image = icon_photo  # Prevent image from being garbage collected
                weather_icon.configure(image=icon_photo)
            except Exception as e:
                print(f"Error loading icon: {e}")

         

         

        
#WIND TAB --------------------------------------------------------
        mph_wind = response["wind"]["speed"]
        wind_mph.configure(text=f"Wind : {mph_wind} mph")

        try:
            wind_gust = response["wind"]["gust"]
            wind_gust_mph.configure(text=f"Gust : {wind_gust} mph")
        except KeyError:
            wind_gust_mph.configure(text=f"Gust : 0 mph")
        
        wind_direction1 = response["wind"]["deg"]
        direction_wind = get_wind_direction(wind_direction1)
        wind_direction.configure(text=f"{direction_wind}")

           #Wind Picture
        my_img = ck.CTkImage(dark_image=Image.open("wind_icon.jpeg"),size=(250,250),)
        wind_icon = ck.CTkLabel(frame_top_right,image=my_img,text="")
        wind_icon.place(x=25,y=35)



         #Feels LIKE 
            

#Sunrise/Sunset Tab===================================================================================================
        sunrise_pic = ck.CTkImage(dark_image=Image.open("SunRise.jpeg"),size=(100,100),)
        sunrise_icon = ck.CTkLabel(frame_bottom_middle,image=sunrise_pic,text="")
        sunrise_icon.place(x = 20, y=160)

        sunset_pic = ck.CTkImage(dark_image=Image.open("SunSet.jpeg"),size=(110,110),)
        sunset_icon = ck.CTkLabel(frame_bottom_middle,image=sunset_pic,text="")
        sunset_icon.place(x = 140, y=157)

        #Putting in the times 
        sunset_time = str(dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone']))
        sunset_time = sunset_time[10:16]

        final_time_sunset = convert_to_standard_time(sunset_time)   

        sunset_time_place = ck.CTkLabel(frame_bottom_middle, text=final_time_sunset, font=("Comfortaa", 24))
        sunset_time_place.place(x=147, y = 115)


        
        sunrise_time = str(dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone']))
        sunrise_time = sunrise_time[10:16]

        final_time_sunrise = convert_to_standard_time(sunrise_time)   
        
        sunrise_time_place = ck.CTkLabel(frame_bottom_middle, text=final_time_sunrise,font=("Comfortaa", 25) )
        sunrise_time_place.place(x=30, y = 114)
        
        
        


        

    else:
        # Handle the case when the response doesn't have the expected structure
        print("Invalid response structure")
        if response:
            print(response)  # Print the actual response for inspection














# GUI using CustomTkinter
root = ck.CTk()

# Setting the Appearance
ck.set_appearance_mode("dark")
ck.set_default_color_theme("blue")

# The Title and Size of the GUI
root.title('SkySync')
root.geometry("1200x750")

frame_left_column = ck.CTkFrame(master=root,
                                width=225, height=799,
                                corner_radius=0,
                                bg_color='#18191A',border_color='#18191A',
                                  border_width=2
                               )
frame_left_column.place(x=9, y=9)
frame_top_middle = ck.CTkFrame(master=root,
                               width=300, height=300,
                               corner_radius=0,
                               bg_color="black",
                               border_color='#18191A',
                                  border_width=2)
frame_top_middle.place(x=275, y=75)
frame_top_right = ck.CTkFrame(master=root,
                              height=300, width=530,
                              corner_radius=0,
                              bg_color="black",
                              border_color='#18191A',
                                  border_width=2)
frame_top_right.place(x=620, y=75)
frame_bottom_left = ck.CTkFrame(master=root,
                                width=258.33, height=270,
                                corner_radius=0,
                                bg_color="black",
                                border_color='#18191A',
                                  border_width=2)
frame_bottom_left.place(x=275, y=425)
frame_bottom_middle = ck.CTkFrame(master=root,
                                  width=258.33, height=270,
                                  corner_radius=0,
                                  bg_color="black",
                                  border_width=2,
                                  border_color='#18191A')
frame_bottom_middle.place(x=583.33, y=425)
frame_bottom_right = ck.CTkFrame(master=root,
                                  width=258.33, height=270,
                                  corner_radius=2,
                                  bg_color="black",
                                  border_width=2,
                                  border_color='#18191A')
frame_bottom_right.place(x=891.66, y=425)

title = ck.CTkLabel(root, text="SkySync's Weather Dashboard", font=("Comfortaa", 20))
title.place(x=250, y=25)













# CURRENTLY TAB ----------------------------------------------------------------------------------------------
weather_icon = ck.CTkLabel(frame_top_middle, image=None, text="")
weather_icon.place(x=6, y=50)

current_date = ck.CTkLabel(frame_top_middle, text="", font=("comfortaa", 10))
current_date.place(x=19, y=37)

Daily_Title = ck.CTkLabel(frame_top_middle, text="Currently", font=("Comfortaa", 30))
Daily_Title.place(x=15, y=3)

current_temp = ck.CTkLabel(frame_top_middle, text="", font=("Comfortaa", 60))
current_temp.place(x=150, y=80)

selected_city = ck.CTkLabel(frame_top_middle, text="", font=("Verdana", 20))
selected_city.place(x=15, y=166)

city_long = ck.CTkLabel(frame_top_middle, text="", font=("comfortaa", 10))
city_long.place(x=15, y=190)

temp_min = ck.CTkLabel(frame_top_middle, text="", font=("Verdana", 15))
temp_min.place(x=180, y=220)
temp_max = ck.CTkLabel(frame_top_middle, text="", font=("Verdana", 15))
temp_max.place(x=180, y=200)








wind_title = ck.CTkLabel(frame_top_right, text="Wind", font=("Comfortaa", 30))
wind_title.place(x=3, y=3)
wind_mph = ck.CTkLabel(frame_top_right, text="", font=("Verdana", 20))
wind_mph.place(x=300,y=80)
wind_gust_mph = ck.CTkLabel(frame_top_right, text="", font=("Verdana", 20))
wind_gust_mph.place(x=300,y=120)
wind_direction = ck.CTkLabel(frame_top_right, text="", font=("Comfortaa", 45))
wind_direction.place(x=350, y=170)




sunriseset_title = ck.CTkLabel(frame_bottom_middle, text="Sunrise | Sunset", font=("Comfortaa", 30))
sunriseset_title.place(x=3, y=3)

highlow_title = ck.CTkLabel(frame_bottom_left, text="Feels Like", font=("Comfortaa", 30))
highlow_title.place(x=3, y=3)

feelslike_title = ck.CTkLabel(frame_bottom_right, text="Pressure", font=("Comfortaa", 30))
feelslike_title.place(x=3, y=3)



# Search Box
Choose_Location_TB = ck.CTkLabel(master=frame_left_column, text="Choose Location", font=("Comfortaa", 25))
Choose_Location_TB.place(x=20, y=25)

city_entry = ck.CTkEntry(frame_left_column, placeholder_text="Enter City", justify="center")
city_entry.place(x=39, y=70)
city_entry.bind("<Return>", get_city)

city_entry_button = ck.CTkButton(frame_left_column, text="Search", width=20, command=get_city)
city_entry_button.place(x=80, y=110)

# MainLoop Run
root.mainloop()