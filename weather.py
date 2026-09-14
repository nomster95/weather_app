import sys
import requests
import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(env_path, override=True)
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton)


from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("enter city name: ",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather: " , self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.location_label = QLabel(self)
        self.details_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.resize(450,650)    
        self.setWindowTitle("weather app")
        vbox = QVBoxLayout()
        vbox.setSpacing(10)
        vbox.setContentsMargins(25,20,25,20)

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.location_label)
        vbox.addWidget(self.details_label)


        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.location_label.setAlignment(Qt.AlignCenter)
        self.details_label.setAlignment(Qt.AlignCenter)


        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.location_label.setObjectName("location_label")
        self.details_label.setObjectName("details_label")


        self.setStyleSheet("""
                           
        QWidget {
            background-color: #1e1e2f;
            color: #ffffff;
            font-family: Arial;
                }

        QLabel#city_label {
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            padding-bottom: 5px;
               }

        QLineEdit#city_input {
            font-size: 21px;
            padding: 12px;
            color: #ffffff;
            background-color: #2a2a40;
            border: 2px solid #4dabf7;
            border-radius: 12px;
                }

        QLineEdit#city_input:focus {
            border: 2px solid #4dabf7;
                }

        QPushButton#get_weather_button {
            font-size: 20px;
            font-weight: bold;
            color: #ffffff;
            background-color: #339af0;
            padding: 12px;
            border: none;
            border-radius: 12px;
                }

        QPushButton#get_weather_button:hover {
            background-color: #4dabf7;
                }

        QPushButton#get_weather_button:pressed {
            background-color: #1971c2;
                }

        QLabel#temperature_label {
            font-size: 65px;
            font-weight: bold;
            color: #ffd166;
            padding-top: 15px;
                }

        QLabel#emoji_label {
            font-size: 80px;
            padding: 5px;
                }

        QLabel#description_label {
            font-size: 25px;
            font-weight: bold;
            color: #74c0fc;
                }

        QLabel#location_label {
            font-size: 22px;
            font-weight: bold;
            color: #ffffff;
            padding-top: 5px;
                }

        QLabel#details_label {
            font-size: 19px;
            color: #d0d0e0;
            background-color: #2a2a40;
            border: 1px solid #44445c;
            border-radius: 12px;
            padding: 12px;
            margin-top: 5px;
                } 
            


                           
        """)

        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather)

    def get_weather(self):
        api_key = os.getenv("API_KEY")
        city = self.city_input.text().strip()
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
        "q": city,
        "appid": api_key
        }

        try:
            response = requests.get(url , params = params,timeout = 10)
            response.raise_for_status()
            data = response.json()


            if data['cod']==200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized API key:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("City not found:\nNot found")
                case 500:
                    self.display_error("Internal server error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from server")
                case 503:
                    self.display_error("Bad request:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\n no response from server") 
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")   

        except requests.exceptions.ConnectionError:
            self.display_error("Connections Error: \n Check your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")    

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects: \n Check the url")


        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")
            

        




    def display_error(self,message):
        self.temperature_label.setStyleSheet("""   
                                            font-size: 30px;
                                            font-weight: bold;
                                            color: #ffd166;                     
                                             
                                             """)
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
        self.location_label.clear()
        self.details_label.clear()

    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data['main']['temp']
        temperature_c = temperature_k - 273.15
        feels_like_k = data["main"]["feels_like"]
        feels_like_c = feels_like_k - 273.15
        humidity = data["main"]["humidity"]
        weather_id = data['weather'][0]['id']
        self.set_weather_theme(weather_id)
        weather_description = data["weather"][0]["description"]
        city_name = data['name']
        country = data['sys']['country']

        

        self.temperature_label.setText(f"{temperature_c:.0f}℃")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
        self.location_label.setText(f"{city_name}, {country}")
        self.details_label.setText(f"Feels like: {feels_like_c:.0f}℃\n"
                                   f"Humidity: {humidity}%"
                                   
                                   )
        

    def set_weather_theme(self,weather_id):

        if 200 <= weather_id <= 232:
            # Thunderstorm
            self.setStyleSheet("""
            QWidget {
                background-color: #171326;
                color: white;
            }

            QLabel#city_label {
                color: #ffffff;
                font-size: 28px;
                font-weight: bold;
            }

            QLineEdit#city_input {
                background-color: #252039;
                color: white;
                border: 2px solid #8064a2;
                border-radius: 12px;
                padding: 12px;
                font-size: 21px;
            }

            QPushButton#get_weather_button {
                background-color: #7654a3;
                color: white;
                border-radius: 12px;
                padding: 12px;
                font-size: 20px;
                font-weight: bold;
            }

            QLabel#temperature_label {
                color: #d8b4fe;
                font-size: 75px;
                font-weight: bold;
            }

            QLabel#emoji_label {
                font-size: 80px;
            }

            QLabel#description_label {
                color: #c4b5fd;
                font-size: 25px;
                font-weight: bold;
            }

            QLabel#location_label {
                color: white;
                font-size: 22px;
                font-weight: bold;
            }

            QLabel#details_label {
                background-color: #252039;
                color: #ddd6fe;
                border-radius: 12px;
                padding: 12px;
                font-size: 19px;
            }
        """)

        elif 300 <= weather_id <= 321 or 500 <= weather_id <= 531:

            # Rain
            self.setStyleSheet("""
            QWidget {
                background-color: #152238;
                color: white;
            }

            QLabel#city_label {
                color: white;
                font-size: 28px;
                font-weight: bold;
            }

            QLineEdit#city_input {
                background-color: #203450;
                color: white;
                border: 2px solid #4d79a8;
                border-radius: 12px;
                padding: 12px;
                font-size: 21px;
            }

            QPushButton#get_weather_button {
                background-color: #3974a8;
                color: white;
                border-radius: 12px;
                padding: 12px;
                font-size: 20px;
                font-weight: bold;
            }

            QLabel#temperature_label {
                color: #74c0fc;
                font-size: 75px;
                font-weight: bold;
            }

            QLabel#emoji_label {
                font-size: 80px;
            }

            QLabel#description_label {
                color: #8ecae6;
                font-size: 25px;
                font-weight: bold;
            }

            QLabel#location_label {
                color: white;
                font-size: 22px;
                font-weight: bold;
            }

            QLabel#details_label {
                background-color: #203450;
                color: #dbeafe;
                border-radius: 12px;
                padding: 12px;
                font-size: 19px;
            }
        """)

        elif 600 <= weather_id <= 622:
            # Snow
            self.setStyleSheet("""
            QWidget {
                background-color: #dce9f2;
                color: #17212b;
            }

            QLabel#city_label {
                color: #17212b;
                font-size: 28px;
                font-weight: bold;
            }

            QLineEdit#city_input {
                background-color: #f5faff;
                color: #17212b;
                border: 2px solid #91b6cc;
                border-radius: 12px;
                padding: 12px;
                font-size: 21px;
            }

            QPushButton#get_weather_button {
                background-color: #5b8fa8;
                color: white;
                border-radius: 12px;
                padding: 12px;
                font-size: 20px;
                font-weight: bold;
            }

            QLabel#temperature_label {
                color: #39708f;
                font-size: 75px;
                font-weight: bold;
            }

            QLabel#emoji_label {
                font-size: 80px;
            }

            QLabel#description_label {
                color: #39708f;
                font-size: 25px;
                font-weight: bold;
            }

            QLabel#location_label {
                color: #17212b;
                font-size: 22px;
                font-weight: bold;
            }

            QLabel#details_label {
                background-color: #f5faff;
                color: #39505f;
                border-radius: 12px;
                padding: 12px;
                font-size: 19px;
            }
        """)

        elif 701 <= weather_id <= 781:
            # Fog / Mist / Haze / Wind
            self.setStyleSheet("""
            QWidget {
                background-color: #30343b;
                color: white;
            }

            QLabel#city_label {
                color: white;
                font-size: 28px;
                font-weight: bold;
            }

            QLineEdit#city_input {
                background-color: #41464e;
                color: white;
                border: 2px solid #777d85;
                border-radius: 12px;
                padding: 12px;
                font-size: 21px;
            }

            QPushButton#get_weather_button {
                background-color: #69717a;
                color: white;
                border-radius: 12px;
                padding: 12px;
                font-size: 20px;
                font-weight: bold;
            }

            QLabel#temperature_label {
                color: #d8dee4;
                font-size: 75px;
                font-weight: bold;
            }

            QLabel#emoji_label {
                font-size: 80px;
            }

            QLabel#description_label {
                color: #c5ccd3;
                font-size: 25px;
                font-weight: bold;
            }

            QLabel#location_label {
                color: white;
                font-size: 22px;
                font-weight: bold;
            }

            QLabel#details_label {
                background-color: #41464e;
                color: #d8dee4;
                border-radius: 12px;
                padding: 12px;
                font-size: 19px;
            }
        """)

        elif weather_id == 800:
            # Clear sky
            self.setStyleSheet("""
            QWidget {
                background-color: #172554;
                color: white;
            }

            QLabel#city_label {
                color: white;
                font-size: 28px;
                font-weight: bold;
            }

            QLineEdit#city_input {
                background-color: #23366f;
                color: white;
                border: 2px solid #5b7cdb;
                border-radius: 12px;
                padding: 12px;
                font-size: 21px;
            }

            QPushButton#get_weather_button {
                background-color: #f59e0b;
                color: white;
                border-radius: 12px;
                padding: 12px;
                font-size: 20px;
                font-weight: bold;
            }

            QLabel#temperature_label {
                color: #ffd166;
                font-size: 75px;
                font-weight: bold;
            }

            QLabel#emoji_label {
                font-size: 80px;
            }

            QLabel#description_label {
                color: #93c5fd;
                font-size: 25px;
                font-weight: bold;
            }

            QLabel#location_label {
                color: white;
                font-size: 22px;
                font-weight: bold;
            }

            QLabel#details_label {
                background-color: #23366f;
                color: #dbeafe;
                border-radius: 12px;
                padding: 12px;
                font-size: 19px;
            }
        """)

        elif 801 <= weather_id <= 804:
            # Clouds
            self.setStyleSheet("""
            QWidget {
                background-color: #263445;
                color: white;
            }

            QLabel#city_label {
                color: white;
                font-size: 28px;
                font-weight: bold;
            }

            QLineEdit#city_input {
                background-color: #354457;
                color: white;
                border: 2px solid #718096;
                border-radius: 12px;
                padding: 12px;
                font-size: 21px;
            }

            QPushButton#get_weather_button {
                background-color: #64748b;
                color: white;
                border-radius: 12px;
                padding: 12px;
                font-size: 20px;
                font-weight: bold;
            }

            QLabel#temperature_label {
                color: #e2e8f0;
                font-size: 75px;
                font-weight: bold;
            }

            QLabel#emoji_label {
                font-size: 80px;
            }

            QLabel#description_label {
                color: #cbd5e1;
                font-size: 25px;
                font-weight: bold;
            }

            QLabel#location_label {
                color: white;
                font-size: 22px;
                font-weight: bold;
            }

            QLabel#details_label {
                background-color: #354457;
                color: #e2e8f0;
                border-radius: 12px;
                padding: 12px;
                font-size: 19px;
            }
        """)    

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <=232:
            return "⛈️"
        elif 300 <= weather_id <=321:
            return "🌦️"
        elif 500 <= weather_id <=531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <=741:
            return "🌫️"
        
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""
        
        


if __name__ == "__main__":      
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())




