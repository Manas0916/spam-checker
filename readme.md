# Django Project

This is a Django project with a REST API.
Make sure you have python and pip installed in local system

## Requirements
This project requires Python 3.6 or later and the following Python packages:

- asgiref>=3.8.1
- Django>=5.0.6
- djangorestframework>=3.15.1
- Faker>=25.8.0
- python-dateutil>=2.9.0.post0
- six>=1.16.0
- sqlparse>=0.5.0

## Installation
1. Navigate to the project directory.
2. Install the required packages using pip:

```bash
pip install -r requirements.txt
```

# Running the Project
1. Apply the migrations:

``` bash
python manage.py migrate 
```

# OPTIONAL - New data Base dump -
If you want a new data base dump, then delete the sqlite file and again migrate the tables.
After that, run the script for dumping sample data - 
For running the script - ``` python populate_data.py ``` (Optional Step)



2. Run the server:
``` bash 
python manage.py runserver
```
The server will start on http://127.0.0.1:8000/.




# For API Testing
Make sure for testing APIs,  you include auth details in the Auth section in POSTMAN or thunderclient
1. Select Basic Authentication
2. Put the username and password of any registered user. 
3. The password for every user will be ``` password123 ``` if you run the script for dumping data into db.
PS- You can try ```james44``` as the user for testing.


# API Documentation

This provides information about the API endpoints of the Django project.

## User Registration

- Endpoint: `/register/`
- Method: `POST`
- Description: Register a new user.
- Request Body: 
    - `username`: The username of the user.
    - `password`: The password of the user.

## User Login

- Endpoint: `/login/`
- Method: `POST`
- Description: Login a user.
- Request Body: 
    - `username`: The username of the user.
    - `password`: The password of the user.

## Contact List

- Endpoint: `/contacts/`
- Method: `GET`
- Description: Get the list of contacts for the authenticated user.

## Mark as Spam

- Endpoint: `/mark-spam/<str:phone_number>/`
- Method: `POST`
- Description: Mark a contact as spam.

## Check Spam

- Endpoint: `/check-spam/<str:phone_number>/`
- Method: `GET`
- Description: Check if a contact is marked as spam.

## Search

- Endpoint: `/search/`
- Method: `GET`
- Description: Search for a contact by name or phone number.
- Query Parameters: 
    - `search_by`: The field to search by. Can be 'name' or 'phone'.
    - `query`: The search query.

## Detailed Search

- Endpoint: `/search_details/<str:phone_number>/`
- Method: `GET`
- Description: Get detailed information about a contact by phone number.