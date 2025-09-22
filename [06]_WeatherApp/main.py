import sys
import os
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from dotenv import load_dotenv # For loading environment variables from .env


class WeatherApp(QWidget):
    """
     A simple weather application using PyQt5 and OpenWeatherMap API.

    Features:
    - Takes a city name as input
    - Fetches real-time weather data from OpenWeatherMap API
    - Displays temperature, weather description, and corresponding emoji
    - Handles errors gracefully with user-friendly messages
    - Loads API key from .env file for security.
    """

    def __init__(self):
        """Initialize the WeatherApp UI and components."""
        super().__init__()
        # UI elements
        self.city_label = QLabel("Enter City Name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        # Setup the UI
        self.initUI()

    def initUI(self):
        """Set up the window layout, styles, and signal connections."""
        self.setWindowTitle("Weather App")

        # Vertical layout for organizing widgets
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        # Aligning text and inputs centrally
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Assigning object names for styling with Qt stylesheets
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Styling the UI using CSS-like syntax for a polished look
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 30px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 30px;
            }
            QPushButton#get_weather_button{
                font-size: 20px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 65px;
            }
            QLabel#emoji_label{
                font-size: 90px;
                font-family: Segoe UI Emoji;
            }
            QLabel#description_label{
                font-size: 40px;
            }
        """)

        # Connect button click event to weather-fetching logic
        self.get_weather_button.clicked.connect(self.get_weather)

        # Trigger get_weather when Enter/Return is pressed in the city_input field
        self.city_input.returnPressed.connect(self.get_weather)

    def get_weather(self):
        """
        Fetch weather data from OpenWeatherMap API based on city input.
        """
        load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv("OPENWEATHER_API_KEY")
        city_name = self.city_input.text().strip()  # Remove leading/trailing spaces

        # Construct the API URL
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

        """
        Displays weather data or error messages depending on the API response.
        """
        try:
            # Send GET request to the API
            response = requests.get(url)
            response.raise_for_status()  # Raise error for bad HTTP responses
            data = response.json()

            # If response code is 200, weather data exists for this city
            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            # Handling specific HTTP error codes
            match response.status_code:
                case 400:
                    self.display_error(
                        "Bad request:\nPlease check your city name")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error(
                        "Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error(
                        "Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nService is down")
                case 504:
                    self.display_error(
                        "Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")

        # Additional network-related error handling
        except requests.exceptions.ConnectionError:
            print("Connection Error:\nCheck your Internet Connection")
        except requests.exceptions.Timeout:
            print("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            print("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            print(f"Something went wrong:\n{req_error}")

    def display_error(self, message):
        """
        Display error message in the temperature label and clear weather info.
        Args:
            message (str): Error message to display
        """
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        """
        Display weather information including temperature, description, and emoji.
        Args:
            data (dict): Weather data JSON returned from API
        """
        self.temperature_label.setStyleSheet("font-size: 65px;")

        # Extract temperature (in Kelvin) and convert to Celsius/Fahrenheit
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15  # Kelvin to Celsius
        temperature_f = (temperature_k - 273.15) * 9 / \
            5 + 32  # Kelvin to Fahrenheit

        # Extract weather condition details
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        # Update UI with weather data
        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(f"{weather_description}")

    @staticmethod
    def get_weather_emoji(weather_id):
        """
        Map weather condition codes to emojis for visual representation.
        Args:
            weather_id (int): Weather condition ID from OpenWeatherMap API
        Returns:
            str: Emoji representing the weather condition
        """

        if 200 <= weather_id <= 232:
            return "⛈️"  # thunderstorm
        elif 300 <= weather_id <= 321:
            return "🌦️"  # drizzle
        elif 500 <= weather_id <= 531:
            return "🌧️"  # rain
        elif 600 <= weather_id <= 622:
            return "❄️"  # snow
        elif 701 <= weather_id <= 741:
            return "🌫️"  # mist or fog
        elif weather_id == 762:
            return "🌋"  # volcanic ash
        elif weather_id == 771:
            return "💨"  # squall - violent gust of wind
        elif weather_id == 781:
            return "🌪️"  # tornado
        elif weather_id == 800:
            return "☀️"  # clear sky
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""


if __name__ == "__main__":
    # Entry point: Create the application and run the event loop
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())