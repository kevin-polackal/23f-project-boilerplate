from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


users = Blueprint('users', __name__)

# VARIABLES:
    # -> age
    # -> isAdmin
    # -> userName
    # -> (primary key) userID

# Get all the users from the database with their variables.
@users.route('/users', methods=['GET'])
def get_users():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of users
    cursor.execute('SELECT userID, userName, isAdmin, age FROM User')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# GET a specific user based on their userID
@users.route('/users/<userID>', methods=['GET'])
def get_a_user(userID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of users
    # Cursor executes sql command by dynamically passing userID from request to get_a_user
    cursor.execute(f'SELECT userID, userName, isAdmin, age FROM User WHERE userID = {userID}')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# GET a specific user based on their userID
@users.route('/users/reports/<userID>', methods=['GET'])
def get_a_user_report(userID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of users
    # Cursor executes sql command by dynamically passing userID from request to get_a_user
    cursor.execute(f'SELECT reporterID, reportID, content FROM Report WHERE offenderID = {userID}')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# CREATE a user
@users.route('/users', methods=['POST'])
def add_new_user():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    username = the_data['userName']
    admin = the_data['isAdmin']
    age = the_data['age']

    # Constructing the query
    query = f'INSERT INTO User (userName, isAdmin, age) VALUES ("{username}", "{admin}", {age})'
    current_app.logger.info(query)


    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Update a user based on their ID
@users.route('/users/<userID>', methods=['PUT'])
def update_user(userID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    username = the_data['userName']
    admin = the_data['isAdmin']
    age = the_data['age']

    username = username.replace("'", "''")

    # Constructing the query
    # username.replace("'", "''") is used to escape any single quotes within the username variable by 
    # replacing them with double single quotes. This is done to prevent SQL injection
    #  by ensuring that any single quotes in the username are treated as data, not as part of the SQL query.
    query = f"UPDATE User SET userName = '{username}', isAdmin = '{admin}', age = {age} WHERE userID = {userID}"
    current_app.logger.info(query)


    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# DELETE a user based on their ID
@users.route('/users/<userID>', methods=['DELETE'])
def delete_user(userID):
    
    # executing and committing the deletion statement 
    cursor = db.get_db().cursor()
    cursor.execute(f'DELETE FROM User WHERE userID = {userID}')
    db.get_db().commit()
    
    return 'Success!'

# GET the roles for a user based on their ID
@users.route('/users/<userID>/roles', methods=['GET'])
def get_user_roles(userID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(f'SELECT projectID, role FROM Role WHERE userID = {userID}')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)
