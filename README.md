# treasury-yields

A small Django project that pulls the current treasury yields, plots them on a curve, allows users to submit
orders and display all past orders.

This app uses the US Dept of Treasure XML feed for current treasury yields.

## Setup Guide

To set up this repo locally, you will have to follow these steps. They are taken from the [Django documentation](https://docs.djangoproject.com/en/6.0/topics/install/#installing-official-release).
There are a few assumptions before starting:

- You have python (and pip) installed already.
- If `python` points to Python 2, use `python3` instead.

### Setup Steps

1. Clone repo
    1. `git clone https://github.com/bryanpinkley/treasury-yields.git`
2. Navigate to the treasury-yields directory
    1. `cd treasury-yields`
3. Set up venv
    1. Create virtual environment: `python -m venv .venv`
    2. Activate: `source .venv/bin/activate`
   3.  Additional [Venv instructions](https://docs.python.org/3/tutorial/venv.html) if needed
4. Install Django and requests library
    1. `python -m pip install -r requirements.txt`
5. Run migrations to set up the initial database
    1. `python manage.py migrate`
6. Create a superuser
    1. `python manage.py createsuperuser`
    2. Enter an example username, email, and password
7. Run the local Django server
    1. `python manage.py runserver`
8. View in browser
    1. http://localhost:8000/yields/
9. Stop the server in the terminal with Control-C

## Explanation of app

### Web Interface

The base web page is at http://localhost:8000/yields/. This page fetches the current treasury yields and plots it on a
curve.
From this page, you can use the buttons to navigate to the [order page](http://localhost:8000/yields/order/)
or [past orders](http://localhost:8000/yields/history/) page.

Additionally, there is a Django Admin page at http://localhost:8000/admin/ that lets you manually edit the User and
Order instances.

### Code

Starting at the root directory, there are two Django components:

- `mysite`: Contains Django code used for setup and configuration of the project.
- `yields`: Contains all the code for the yields app, such as business logic, templates, and URLs.

Breaking down how the app is structured in `yields`:

- `apps.py`: Configures the "yields" app within Django.
- `models.py`: Defines the Order model, which sets up the structure of the database table.
- `urls.py`: Defines URL patterns for the app.
- `views.py`: Handles HTTP requests and responses for the app.
- `behaviors.py`: Contains custom business logic for the app.
- `constants.py`: Houses constants used throughout the app.
- `admin.py`: Defines admin configurations for the Order model.
- `migrations` folder: Holds migration files for the app, which create the tables required.
- `templates` folder: Contains HTML templates rendered by the views.

## Potential Improvements

Given the time constraint of this project, I could not address all the features I would like to implement.
Below are some of the tasks that I would implement to improve the app:

- Error handling
    - If the XML response returns an error, or data in an unexpected format, the app should handle it gracefully and
      provide meaningful error messages to the web page.
- Unit tests
    - Automated unit tests can be implemented for the `behaviors.py` and `views.py` files to ensure that edge cases are
      covered.
- Implement a cache for the yield data
    - In my testing, the yield data from the XML feed takes ~10 seconds to load, and this happens for both the home
      page, and the order page. If a caching system was implemented, then the data could be fetched once a day, and this
      would significantly increase the user experience.