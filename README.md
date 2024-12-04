# Cafe Finder Web App
## Overview
The Cafe Finder Web App is a Flask-based application designed to manage a database of cafes. It provides both a user-friendly web interface and RESTful APIs for retrieving, adding, editing, and deleting cafe data. The app uses SQLite as its database and integrates with Flask-Bootstrap for improved UI styling.

---

## Features

### Web Interface
* View a list of all cafes on the homepage.
* Search for cafes by location.
* Get a random cafe recommendation.
* Add new cafes to the database.
* Edit details of existing cafes.
* Delete cafes marked as closed.

### APIs
* **Get All Cafés**: Retrieve all cafes in JSON format (/all).
* **Random Cafe**: Fetch a random cafe in JSON format (/random-cafe-api).
* **Search Cafe**: Search for cafes at a specific location via an API (/search-cafe-api?loc=<location>).
* **Add Cafe**: Add a new cafe via POST request (/add-cafe-api).

---

## Tech Stack
* **Backend**: Flask
* **Database**: SQLite
* **Frontend**: Flask-Bootstrap
* **Forms**: Flask-WTF (for form validation)
* **API Responses**: Flask-JSONify

---

## Prerequisites
Ensure you have the following installed:
* Python 3.7+
* pip (Python package manager)

---

## Setup Instructions
1. Clone the Repository
    ```commandline
    git clone https://github.com/your-username/cafe-finder.git
    cd cafe-finder
    ```

2. Set Up Virtual Environment
    ```commandline
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install Dependencies

4. Create the Database

   * Open a Python shell:
    ```commandline
   python
    ```

   * Run the following:
   ```python
   import sqlite3
   db = sqlite3.connect('cafes.db')
   cursor = db.cursor()
   cursor.execute("""
   CREATE TABLE cafes (
       id INTEGER PRIMARY KEY NOT NULL,
       name VARCHAR(500) UNIQUE NOT NULL,
       map_url VARCHAR(500) NOT NULL,
       img_url VARCHAR(500) NOT NULL,
       location VARCHAR(500) NOT NULL,
       has_sockets BOOLEAN NOT NULL,
       has_toilet BOOLEAN NOT NULL,
       has_wifi BOOLEAN NOT NULL,
       can_take_calls BOOLEAN NOT NULL,
       seats VARCHAR(100) NOT NULL,
       coffee_price VARCHAR(100) NOT NULL
   )
   """)
   db.commit()
   db.close()
   ```
   
5. Run the App
    ```commandline
    flask run
    ```

6. Access the App Open http://127.0.0.1:5000 in your browser.

---

## Project Structure
```graphql
cafe-finder/
│
├── templates/               # HTML templates for rendering pages
│   ├── index.html
│   ├── random.html
│   ├── search_by_location.html
│   ├── add_cafe.html
│   ├── edit_cafe.html
│
├── static/                  # Static files (e.g., CSS, JS, images)
│
├── forms.py                 # Flask-WTF forms for validation
├── app.py                   # Main Flask application
├── cafes.db                 # SQLite database file
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
```

---

## API Endpoints
1. Get All Cafés
    * **URL**: `/all`
    * **Method**: `GET`
    * **Response**: JSON containing all cafes.

2. Random Cafe
    * **URL**: `/random-cafe-api`
    * **Method**: `GET`
    * **Response**: JSON containing a random cafe.

3. Search Cafés by Location
    * **URL**: `/search-cafe-api?loc=<location>`
    * **Method**: `GET`
    * **Response**: JSON containing cafes at the specified location or a 404 error if none are found.

4. Add a Cafe
   * **URL**: **/add-cafe-api**
   * **Method**: `POST`
   * **Payload**: Form data with the following fields:

     * `name`
     * `map_url`
     * `img_url`
     * `location`
     * `has_sockets`
     * `has_toilet`
     * `has_wifi`
     * `can_take_calls`
     * `seats`
     * `coffee_price`
     
   * **Response**: JSON with a success message.

---

## Contributing
1. Fork the repository.
2. Create a new feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

## License
This project is licensed under the MIT License.