# Desk Booking Web Application

> This desk booking web application provides a full stack solution to booking desks. This is especially needed in the current world climate where most offices use a hot-desk system. This provides the soloution with features such as user accounts, interactive desk booking/viewing and administration to view the database straight from the frontend UI.
> 
## App Screenshots

|                                                                                    Desk Booking App Homepage|                                                                                   Desk Booking Page |                                                                                My Bookings Page                                                                                |                                                                             Admin Control Panel                                                                              |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| <img src="https://raw.githubusercontent.com/Brandon-D-2020/Desk-Booking-Web-App/master/.github/home-page.png" title="Desk Booking App Homepage" width="100%" crossorigin> | <img src="https://raw.githubusercontent.com/Brandon-D-2020/Desk-Booking-Web-App/master/.github/desk-booking-page.png" title="Desk Booking Page" width="100%" crossorigin> | <img src="https://raw.githubusercontent.com/Brandon-D-2020/Desk-Booking-Web-App/master/.github/my-bookings-page.png" title="My Bookings Page" width="100%" crossorigin> | <img src="https://raw.githubusercontent.com/Brandon-D-2020/Desk-Booking-Web-App/master/.github/admin-page.png" title="Admin Control Panel" width="100%" crossorigin> |

# Folder Structure
```
└── desk-booking-web-app/
    ├── backend/
    │   ├── app/
    │   │   ├── tests/ # API Tests
    │   │   │   ├── ...
    │   │   ├── __init__.py
    │   │   ├── auth.py
    │   │   ├── crud.py
    │   │   ├── database.py
    │   │   ├── main.py
    │   │   ├── models.py
    │   │   ├── schemas.py
    │   │   └── security.py
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── frontend/
    │   ├── public/
    │   │   ├── ...
    │   ├── src/
    │   │   ├── components/
    │   │   │   ├── admin/ # Admin managment pages
    │   │   │   ├── auth/ # Login and Register pages
    │   │   │   ├── desk-booking/ # Desk booking pages
    │   │   │   ├── header/ # App bar
    │   │   │   └── services/ # API call functions
    │   │   ├── ...
    │   ├── .gitignore
    │   ├── Dockerfile
    │   ├── package-lock.json
    │   └── package.json
    ├── .gitignore
    └── docker-compose.yml
  ```
# Developing

## Technolgies

 - [FastAPI](https://fastapi.tiangolo.com/)
 - [React](https://reactjs.org/)
 - [PosgreSQL](https://www.postgresql.org/)

## Prerequisites
#### Clone the project
    git clone https://github.com/Brandon-D-2020/Desk-Booking-Web-App.git
#### 

## Run using docker

 - [Install docker](https://docs.docker.com/get-docker/) on your device
 - run `docker-compose build --no-cache` in the root directory
 - run `docker-compose up` in the root directory


## Run locally
Run these in order for local setup, this is assuming you have VSCode installed and have opened the soloution.
#### PostgreSQL

 - Download and install [PostgreSQL](https://www.postgresql.org/download/)
 - Set all passwords to **password** or define the enviroment variable **SQLALCHEMY_DATABASE_URL** to your custom database URL

#### Backend
 - [Install the latest version](https://www.python.org/downloads/) of Python 3.9.x
 - [Create a venv](https://code.visualstudio.com/docs/python/environments) for running the API
 - Install dependencies
 - `cd ./backend/`
 - `pip install -r requirements.txt`
 - Start the uvicorn server on port 8000 using `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
#### Frontend
 - Install the [latest version of Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
 - Install dependencies
 - `cd ./frontend/`
 - `npm install`
 - Start the development server using `npm start`
#### Testing and Code Coverage
Run all the command in the venv you set up previously
 - `cd ./backend/` 
 - `pytest -vv`
 - `coverage run -m pytest `
 - `coverage report`
## Accessing the UI and API
After running the application you can access the various components through these URLs.
*Note: Swagger docs are recommended*
 - UI: http://localhost:3000/
 - API Swagger Docs: http://localhost:8000/docs#/
 - API Redoc Docs: http://localhost:8000/redoc