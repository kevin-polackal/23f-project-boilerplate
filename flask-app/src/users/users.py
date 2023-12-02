from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


users = Blueprint('users', __name__)

# Get all the projects from the database with their title and description
@users.route('/users', methods=['GET'])
def get_users():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
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

@users.route('/users/<userID>', methods=['GET'])
def get_a_user(userID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT userID, userName, isAdmin, age FROM User WHERE userID = {}'.format(userID))

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
    query = 'INSERT INTO User (userName, isAdmin, age) VALUES ("'
    query += username + '", "'
    query += str(admin) + '", '
    query += str(age) + ')'
    current_app.logger.info(query)


    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

@users.route('/users/<userID>', methods=['PUT'])
def update_user(userID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    username = the_data['userName']
    admin = the_data['isAdmin']
    age = the_data['age']

    # Constructing the query
    query = "UPDATE User SET userName = '{}', isAdmin = '{}', age = {} WHERE userID = {}".format(username.replace("'", "''"), admin, age, userID)
    current_app.logger.info(query)


    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


@users.route('/users/<userID>', methods=['DELETE'])
def delete_user(userID):
    
    # executing and committing the deletion statement 
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM User WHERE userID = {0}'.format(userID))
    db.get_db().commit()
    
    return 'Success!'

@users.route('/users/<userID>/roles', methods=['GET'])
def get_user_roles(userID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT projectID, role FROM Role WHERE userID = {0}'.format(userID))

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
'''
# Get specific information regarding a project
@projects.route('/projects/<projectID>', methods=['GET'])
def get_project(projectID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT title, overview, funding FROM Project WHERE projectID = {0}'.format(projectID))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)
'''