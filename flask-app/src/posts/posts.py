from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


posts = Blueprint('posts', __name__)

# Post Variables:
    # -> userName
    # -> title
    # -> content
    # -> primary key (postID)


# Get all the posts from the database with their title and content
@posts.route('/posts', methods=['GET'])
def get_posts():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of posts    
    cursor.execute('''
    SELECT User.userName, User.age, Post.title, Post.content, Post.createdAt 
    FROM Post 
    JOIN User ON Post.userID = User.userID 
    ORDER BY Post.createdAt DESC
    LIMIT 100
''')

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

# CREATE a post for this user
@posts.route('/posts/<userID>', methods=['POST'])
def new_post(userID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    title = the_data['title']
    content = the_data['content']
    
    title = title.replace('"', '\\"')
    content = content.replace('"', '\\"')

    # Constructing the query
    query = f'INSERT INTO Post (userID, title, content) VALUES ("{userID}", "{title}", "{content}")'
    current_app.logger.info(query)



    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# UPDATE a post for a given user
@posts.route('/posts/<userID>/<postID>', methods=['PUT'])
def update_user_post(userID, postID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    content = the_data['content']
    title = the_data['title']

    content = content.replace("'", "''")
    title = title.replace("'", "''")

    # Constructing the query
    query = f"UPDATE Post SET content = '{content}', title = '{title}' WHERE userID = {userID} AND postID = {postID}"
    current_app.logger.info(query)


    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# DELETE a post for a given user
@posts.route('/posts/<userID>/<postID>', methods=['DELETE'])
def delete_post(postID, userID):
    
    # executing and committing the deletion statement 
    cursor = db.get_db().cursor()
    cursor.execute(f'DELETE FROM Post WHERE postID = {postID} AND userID = {userID}')
    db.get_db().commit()
    
    return 'Success!'

# DELETE all posts for a user based on their userID
@posts.route('/posts/<userID>/', methods=['DELETE'])
def delete_all_user_posts(userID):
    
    # executing and committing the deletion statement 
    cursor = db.get_db().cursor()
    cursor.execute(f'DELETE FROM Post WHERE userID = {userID}')
    db.get_db().commit()
    
    return 'Success!'

# GET the comments for a given post based on its postID
@posts.route('/posts/<postID>/comments', methods=['GET'])
def get_post_comments(postID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of posts
    cursor.execute(f'SELECT username, content FROM Comment JOIN User on Comment.userID = User.userID WHERE Comment.postID = {postID}')

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

# GET all posts from a given user based on their ID
@posts.route('/posts/<userID>', methods=['GET'])
def get_all_user_posts(userID):
    cursor = db.get_db().cursor()
    cursor.execute(f'SELECT postID, title, content, createdAt FROM Post WHERE userID = {userID}')
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)