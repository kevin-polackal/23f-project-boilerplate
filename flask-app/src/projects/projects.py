from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


projects = Blueprint('projects', __name__)

# Get all the projects from the database with their title and description
@projects.route('/projects', methods=['GET'])
def get_projects():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT projectID, title, overview as description FROM Project')

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

@projects.route('/create-project', methods=['POST'])
def add_new_project():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    description = the_data['overview']
    title = the_data['title']
    funding = the_data['funding']

    # Constructing the query
    query = 'INSERT INTO Project (overview, title, funding) VALUES ("'
    query += description + '", "'
    query += title + '", '
    query += str(funding) + ')'
    current_app.logger.info(query)


    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'



@projects.route('/delete-project/<projectID>', methods=['DELETE'])
def delete_proj(projectID):
    
    # executing and committing the deletion statement 
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Project WHERE projectID = {0}'.format(projectID))
    db.get_db().commit()
    
    return 'Success!'