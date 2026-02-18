from flask import Flask, render_template, request
import requests

# 1️⃣ Create app FIRST
app = Flask(__name__)

# 2️⃣ API configuration
API_KEY = "a1b1c5c4c920df9746a3a460904eea5f"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# 3️⃣ Route
@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None

    if request.method == 'POST':
        city = request.form.get('city')

        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("cod") != 200:
            weather = {"error": data.get("message")}
        else:
            weather = {
                "city": city,
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
                "humidity": data["main"]["humidity"]
            }

    return render_template("index.html", weather=weather)


# 4️⃣ IMPORTANT: Start the server
if __name__ == '__main__':
    app.run(debug=True)

