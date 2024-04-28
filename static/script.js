api_key = 'd4cf8a7a60a0e91e4b8a258029176861'

function fetchWeatherData() {
  const city = document.getElementById('city-name');
  var apiKey = "d4cf8a7a60a0e91e4b8a258029176861";


  const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=d4cf8a7a60a0e91e4b8a258029176861&units=metric`;

  return fetch(url)
   .then(response => {
      if (!response.ok) {
        throw new Error('Error fetching weather data');
      }
      return response.json();
    })
   .then(data => {
      const weatherData = {
        temperature: data.main.temp,
        tempMin: data.main.temp_min,
        tempMax: data.main.temp_max,
        humid: data.main.humidity,
        windSpeed: data.wind.speed,
        windDeg: data.wind.deg,
      };
      console.log(weatherData);
    })
   .catch(error => {
      console.error('Error fetching weather data:', error);
      return null;
    });
}

function updateWeather() {
  fetchWeatherData().then(weatherData => {
    if (weatherData!== null) {

      const temperatureElement = document.getElementById('temperature');
      temperatureElement.innerText = weatherData.temperature;
      const temperatureMinElement = document.getElementById('min-temp');
      temperatureMinElement.innerText = weatherData.tempMin;
      const temperatureMaxElement = document.getElementById('max-temp');
      temperatureMaxElement.innerText = weatherData.tempMax;


      const windSpeedElement = document.getElementById('wind-speed');
      windSpeedElement.innerText = weatherData.windSpeed;
      const windSpeedDirectionElement = document.getElementById('wind-deg');
      windSpeedDirectionElement.innerText = weatherData.windDeg;


      const humidityElement = document.getElementById('humidity');
      humidityElement.innerText = weatherData.humid;
    } else {
      console.error('Weather data is not available');
    }
  });
}


fetchWeatherData();


setInterval(() => updateWeather(), 600000); 

