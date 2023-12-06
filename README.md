Link to the Phase 3 Explainer Video: https://drive.google.com/file/d/15_vB7aXQBcLx2T7g3d8oHWUhfDk_MBoO/view?usp=sharing
# NuBee: The new Opensource of Northeastern
Collabaration is what breeds innovation. NuBee is a platform for students to come together and to work on engaging, passion driven projects. From here you can see what every is up to and the things they are working on. Anyone of any skill level, and any background is welcome!

# Run the containers
`docker compose up -d`

# Overview of Routes
There are 3 main blueprints that have been implemented, Post, User, and Project.

Post Functionality:
* Get all Posts in the Database
* Get the comments on a given post
* Get all the Posts from a given user
* Create a Post for some user
* Update a specific post from a given user
* Delete a specific post from a given user
* Delete all posts from a given user

User Functionality:
* Get all users
* Get a certain user
* Get the reports of a certain user
* Get a given user's roles
* Create a new user
* Update a given user
* Delete a given user

Project Functionality:
* Get all projects
* Get a given project
* Get the milestones of a given project
* Create a project
* Join a project through a role
* Update a given project
* Delete a given project
  

  
# MySQL + Flask Boilerplate Project

This repo contains a boilerplate setup for spinning up 3 Docker containers: 
1. A MySQL 8 container for obvious reasons
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 




