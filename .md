Steps
1. Clone the repository from GitHub: git clone https://github.com/vishwajittidke/real-time-weather-app

2. Install dependencies: pip install -r requirements.txt

3. Set up a virtual environment : python -m venv venv

4. Activate the virtual environment: venv\scripts\activate

5. Configure the PostgreSQL database:

   - Create a database named weather_db.
   - Update the PostgreSQL database credentials in app.py file.

6. Set environment variables in .env file:

   - API_KEY =  OpenWeatherMapAPI Key

7. Run the application: 
      •	python app.py
      OR
      •	flask run
