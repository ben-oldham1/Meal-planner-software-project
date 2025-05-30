# Meal Planner Software Project

**Software Development Project**
**Author: Ben Oldham**

## Running locally

Follow these instructions to setup the project locally. Commands shown are for mac, but the equivalent should work on windows/linux.

1. Clone the repo to your local machine.
2. Open a terminal and activate the python virtual environment:

```
source venv/bin/activate
```

3. Create a .env file to store API keys
```
# Nutritionix API credentials
APP_ID=YOUR_APP_ID
APP_KEY=YOUR_APP_KEY
```

4. Run the development server:

```
python manage.py runserver
```

5. Navigate to `http://127.0.0.1:8000/` and you will see the app homepage.

### Running tests

1. Use the built-in Django test command to run the unit tests

```
python manage.py test
```