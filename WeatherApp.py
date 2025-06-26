import sys
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# create class for weather
class Weather(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("weather.jpg"))
        self.city_label = QLabel("Your City Name : " , self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.discription_label = QLabel(self)
        self.iniUI()

    # Function for interface
    def iniUI(self):
        self.setWindowTitle("Weather App")


        # Vertical widgrt
        vbox = QVBoxLayout() 
        vbox.addWidget(self.city_label)       
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.discription_label)

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.discription_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.get_weather_button.setObjectName('get_weather_button')
        self.temperature_label.setObjectName('temperature_label')
        self.emoji_label.setObjectName('emoji_label')
        self.discription_label.setObjectName('discription_label')
        
        self.setStyleSheet("""
                QLabel,QPushButton{
                           font-family: calibri;
                            }  
                QLabel#city_label{
                           font-size: 45px;
                           font-style: italic
                           }
                QLineEdit#city_input{
                        font-size:40px;
                           }
                QPushButton#get_weather_button{
                           font-size:30px;
                           font-weight: bold;
                           }
                QLabel#temperature_label{
                           font-size:75px;
                           }
                QLabel#emoji_label{
                           font-size: 100px;
                           font-family: Segeo UI emoji;
                           }
                QLabel#discription_label{
                           font-size:50px;
                           }
        """)
        self.get_weather_button.clicked.connect(self.get_weather)
    
    
    def get_weather(self):

        #your unique api key from OpenWeather website
         
        api_key = "a85723f73a364296de4934796f47d93f" 
        # user input
        city = self.city_input.text()
        # formating the string
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200 :
                
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:

            match response.status_code :
                case 400:
                    self.display_error('Bad request \n Please Check your input')
                case 401:
                    self.display_error('Unauthorized\n Invalid Key')
                case 403:
                    self.display_error('Forbidden\n Access denied ')
                case 404:
                    self.display_error('Not Found \n City not found')
                case 500:
                    self.display_error('Internal Server Error \n Please try again later')
                case 502:
                    self.display_error('Bad Gateway\n Invalid ressponse from server')
                case 503:
                    self.display_error('Service Unavailabel\n Server is Down')
                case 504:
                    self.display_error('Gateway Timeout \n No response from server')
                case _:
                    self.display_error(f'HTTP error occurred\n {http_error}')

        except requests.exceptions.ConnectionError:
            self.display_error('Connection error')
        
        except requests.exceptions.Timeout:
            self.display_error("Timeout")
        except requests.exceptions.TooManyRedirects:
            self.display_error("To many redirects")
                   
        except requests.exceptions.RequestException as req_error:
            self.display_error(f'Request error:\n {req_error}')

        # print(data)
    
    
    def display_error(self,message):

        self.temperature_label.setStyleSheet("font-size: 40px;"
                                            #  "color : red;"
                                             "font-weight: bold"
                                            )
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.discription_label.clear()


    def display_weather(self , data):
        temperature_k = data['main']['temp']
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5)- 459.67
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_c:.0f}℃ | {temperature_f:.0f}℉")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.discription_label.setText(weather_description.capitalize())
    
    @staticmethod   
    def get_weather_emoji(weather_id):
        if weather_id >= 200  and weather_id <= 232:
            return "🌩️"
        elif 300 >= weather_id <=321:
            return "🌦️"
        elif weather_id >= 500 and weather_id <= 531:
            return "🌧️"
        elif weather_id >=600 and weather_id <= 622:
            return "❄️"
        elif  weather_id >=701 and weather_id <=741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "🌬️"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif weather_id >= 801 and weather_id <= 804:
            return "☁️"
        else:
            return "--"
        



# Initializing the start(window)
if __name__ =="__main__":
    app = QApplication(sys.argv)
    weather_app = Weather()
    weather_app.show()
    sys.exit(app.exec_())






































































































# developer : Frans M Chokoe
# date : 26 June 2025