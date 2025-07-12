# Orders Platform
This is an Orders Platform that allows users to manage the orders. The platform is built using Django Framework + SQL Server. The platform has the following features:
- User can log in to the platform.
- User can manage the Departments.
- User can manage the Brands.
- User can manage the Providers.
- User can manage the Unit Measure.
- User can manage the Articles.
- User can manage the Orders.

## Requirements
- Python 3.8 or higher
- Django 3.2 or higher
- SQL Server 2017 or higher (optional, for database)
- Docker (optional, for containerization)
- Docker Compose (optional, for containerization)

## Installation
1. Clone the repository
2. Create a virtual environment
   1. `python3 -m venv venv`
   2. `source venv/bin/activate`
3. Install the requirements
   1. `pip install -r requirements.txt`
4. Run the migrations
   1. `python manage.py migrate`
5. Create a superuser
   1. `python manage.py createsuperuser`
6. Run the server
   1. `python manage.py runserver`
7. Open the browser and go to `http://localhost:8000/admin/`
