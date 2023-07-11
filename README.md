# crudoperation
git clone <repository-url>
cd project-directory
create virtual env
python -m venv venv
Activate the virtual environment:venv\Scripts\activate
Install all dependancy:pip install -r requirements.txt
Run the application:set FLASK_APP=app.py
flask run
The application should now be running at http://localhost:5000.
API Endpoints
The application provides the following REST API endpoints:

GET /users: Returns a list of all users.
GET /users/<user_id>: Returns the user with the specified ID.
POST /users: Creates a new user with the specified data.
PUT /users/<user_id>: Updates the user with the specified ID with the new data.
DELETE /users/<user_id>: Deletes the user with the specified ID.

You can use a tool like Postman to interact with the API endpoints:

Send a GET request to http://localhost:5000/users to retrieve all users.
Send a GET request to http://localhost:5000/users/<user_id> to retrieve a specific user.
Send a POST request to http://localhost:5000/users with JSON data to create a new user.
Send a PUT request to http://localhost:5000/users/<user_id> with JSON data to update a user.
Send a DELETE request to http://localhost:5000/users/<user_id> to delete a user.
