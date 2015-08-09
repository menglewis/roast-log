# Roast Log

A simple web application for keeping track of information about Coffee roasts.

## Installation
1. Clone the repository `git clone https://github.com/menglewis/roast-log.git`
2. Install the required libraries `pip install -r requirements.txt`
3. Instantiate the database `python manage.py db init`
4. Create initial migrations and run them `python manage.py db migrate` `python manage.py db upgrade`
5. Run the application server `python manage.py runserver`

## Configuration
Configuration is defined in app/settings.py. The main settings are SECRET_KEY and SQLALCHEMY_DATABASE_URI which in Production should be stored in an environment variable.

## Using the Application
A login is required to start using this application. Registration only requires a username and password.

After signing in, the first step is to add Beans and Roasters. Once there are at least one of each, then you can start recording Roasts.
