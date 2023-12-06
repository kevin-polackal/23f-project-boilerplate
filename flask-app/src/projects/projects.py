from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


projects = Blueprint('projects', __name__)

# VARIABLES:
    # -> Overview
    # -> Title
    # -> Funding
    # -> (primary key) ID

# GET all the projects from the database with their title and description
@projects.route('/projects', methods=['GET'])
def get_projects():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of projects
    cursor.execute('SELECT projectID, title, overview as description, funding FROM Project')

    # grab the column headers from the returned data. Should be projectID, title, overview (desc), and funding
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # Append each project row to the json data to return
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)


# Create or POST a new project
@projects.route('/projects', methods=['POST'])
def add_new_project():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variables of a project:
    description = the_data['overview']
    title = the_data['title']
    funding = the_data['funding']

    # Constructing the project query
    query = f'INSERT INTO Project (overview, title, funding) VALUES ("{description}", "{title}", {funding})'
    query += description + '", "'
    query += title + '", '
    query += str(funding) + ')'
    # Verify the project is in good form
    current_app.logger.info(query)


    # Execute and create the project in the database
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


@projects.route('/projects/join', methods=['POST'])
def join_project():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    projectID = the_data['projectID']
    userID = the_data['userID']
    role = the_data['role']

    # Constructing the query
    query = f'INSERT INTO Role (projectID, userID, role) VALUES ("{projectID}", "{userID}", "{role}")'
    current_app.logger.info(query)


    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


# UPDATE/PUT a project based on its ID

@projects.route('/projects/<projectID>', methods=['PUT'])
def update_proj(projectID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    description = the_data['overview']
    title = the_data['title']
    funding = the_data['funding']
    
    description = description.replace("'", "''")
    title = title.replace("'", "''")

    # Constructing the query
    query = f"UPDATE Project SET overview = '{description}', title = '{title}', funding = {funding} WHERE projectID = {projectID}"
    # Verify query before sending to DB
    current_app.logger.info(query)


    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


# Delete a project based on its ID.
@projects.route('/projects/<projectID>', methods=['DELETE'])
def delete_proj(projectID):
    
    # executing and committing the deletion statement 
    cursor = db.get_db().cursor()
    cursor.execute(f'DELETE FROM Project WHERE projectID = {projectID}')
    db.get_db().commit()
    
    return 'Success!'

# GET the milestones for a project based on its ID.
@projects.route('/projects/<projectID>/milestones', methods=['GET'])
def get_milestones(projectID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of projects
    cursor.execute(f'SELECT projectID, dueDate, completed FROM Milestone WHERE Milestone.projectID = {projectID}')

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

# Get specific information regarding a project
@projects.route('/projects/<projectID>', methods=['GET'])
def get_project(projectID):
    cursor = db.get_db().cursor()
    # Prone to SQL injection, but okay for purposes of MVP
    cursor.execute(f'SELECT title, overview, funding FROM Project WHERE projectID = {projectID}')
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)