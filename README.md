# AugMend Health Project
A technical challenge for the full stack developer position


## Overview
This project aims to develop a login system to collect user data for further analysis. The system provides an interactive interface where users can login/sigup securly,submit their data through a form, and receive insights.

## Technology Stack
- **Backend**: 
Python-Flask, RESTful API
  - Flask is used for setting up the backend server and handling API requests.
- **Frontend**: 
HTML, CSS, JavaScript
  - The frontend is designed with basic HTML and CSS for structure and styling, while JavaScript, including libraries like jQuery, is used for dynamic interactions.
- **Database**: 
MongoDB
  - MongoDB is utilized for storing user queries and responses for analysis.
- **Optional Extensions**:
Use **Parameterized Queries** to prevent common security vulnerabilities
Even though MongoDB does not use SQL, its query language can still be vulnerable. To ensure that all queries are built using parameters rather than constructing queries from concatenated strings or direct user input.
    ```
    # Example of using parameters in PyMongo
    import pymongo

    client = MongoClient()
    db = client.test_database
    collection = db.test_collection

    # Secure way to query MongoDB using user input
    user_input = "example"
    query = {"username": user_input}
    user_data = collection.find_one(query)

    ```
[Link to the video demo](https://www.loom.com/share/ef1890e789484b94b9b8dfbeb70c88a3?sid=5d0284d4-7f08-4223-bfc0-d803da6f96b8)

## Code Explanation and Folder Structure
- `app.py`: The main entry point for the Flask application. It initializes the app and sets up the routes.
- `static/js`: Contains JavaScript files to handle user interactions on the client side.
  - `script.js`: Handles AJAX requests to the server and updates the UI dynamically.
  - `jquery.js`: A library used to simplify DOM manipulation and AJAX calls.
- `templates`: Contains HTML files that define the structure of web pages.
  - `base.html`: The base template including elements common to all pages like header and footer.
  - `home.html`: The main page where users can signup.
  - `login.html`: The page where existing users can login.
  - `questions.html`: The page where users can finish the questions while login.
  - `thanku.html`: The page for user feedback page.
- `user`: A directory containing modules related to user management and survey handling.
  - `models.py`: Defines data models for storing user information.
  - `routes.py`: Contains Flask routes related to user operations.
  - `decorators.py`: Provides decorators for route functions, such as login required decorators.
  - `google_auth_setup.py` for handling Google authentication.
  - `survey_handling.py` for managing user feedback through surveys.

## How to Run
1. **Clone the Repository:**
   ```bash
   git clone [repository-url]
   cd Augmend-project

2. **Set up a Virtual Environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install requirments.txt:**(Python 3.10.8)
   ```bash
   pip install -r requirments.txt

4. **Activate MongoDB:**
   ```bash
   brew services start mongodb-community
   mongo
   use user_login_system
   db.createCollection("users")
   db.createCollection("survey")


Recommend: Download [Studio 3T](https://studio3t.com/download/) for better visual DB experience

4. **Run the app:**
   ```bash
   sudo chomd +x ./run  
   ./run


