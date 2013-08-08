""" 
Use the OpenWeather API (http://openweathermap.org/api) to get the weather for a given city and print out the results
Reddit link: http://www.reddit.com/r/beginnerprojects/comments/1dzbu7/project_whats_the_weather/
"""

import json, http.server, socketserver
from urllib.request import urlopen

def openWeather(city,countryCode,dataType="weather",units="metric"):
	"""
		Queries OpenWeatherMap.org for weather information
	"""

	BASE_PATH = "http://api.openweathermap.org/data/2.5/" + dataType + "?q=" + city

	if countryCode != "":
		BASE_PATH = BASE_PATH + "," + countryCode

	BASE_PATH = BASE_PATH + "&units=" + units
	weather_dict = {}
	error = False

	raw_data = urlopen(BASE_PATH)
	json_string = raw_data.readall().decode('utf-8')
	parsed_data = json.loads(json_string)
	
	
	if "message" in parsed_data:
		for data in parsed_data['message']:
			if "Error" in data:
				error = True

	if error:
		weather_dict["response_type"] = parsed_data["cod"]
		weather_dict["description"] = parsed_data["message"]
	else:
		weather_dict["city_name"] = parsed_data["name"]
		weather_dict["country_code"] = parsed_data["sys"]["country"]
		weather_dict["longitude"] = parsed_data["coord"]["lon"]
		weather_dict["latitude"] = parsed_data["coord"]["lat"]
		weather_dict["response_type"] = parsed_data["cod"]
		if dataType == "weather":
			weather_dict["weather_id"] = parsed_data["weather"][0]["id"]
			weather_dict["weather_main"] = parsed_data["weather"][0]["main"]
			weather_dict["description"] = parsed_data["weather"][0]["description"]
			weather_dict["datetime_string"] = parsed_data["dt"]
			weather_dict["temp_current"] = parsed_data["main"]["temp"]
			weather_dict["temp_min"] = parsed_data["main"]["temp_min"]
			weather_dict["temp_max"] = parsed_data["main"]["temp_max"]
			weather_dict["humidity"] = parsed_data["main"]["humidity"]
			weather_dict["wind_speed"] = parsed_data["wind"]["speed"]
			weather_dict["wind_direction"] = parsed_data["wind"]["deg"]
			weather_dict["wind_gust"] = parsed_data["wind"]["gust"]

		# elif dataType == "forecast":


	return weather_dict

def startServer(PORT=8082):
	"""
	Create webserver to serve HTML page with weather results
	"""
	Handler = http.server.SimpleHTTPRequestHandler
	httpd = socketserver.TCPServer(("", PORT), Handler)

	print("Webserver started on port", PORT)

	# Activate webserver and continue until interrupted by ctrl+c
	httpd.serve_forever()

if __name__ == "__main__":
	startServer()

	# weather_dict = openWeather("Melbourne","AU")
	# print("Location: " + weather_dict["city_name"])
	# print("Description: " + weather_dict["description"])
	# print("Temperature: ",weather_dict["temp_current"], "(Low: ",weather_dict["temp_min"], " , High: ",weather_dict["temp_max"],")")
