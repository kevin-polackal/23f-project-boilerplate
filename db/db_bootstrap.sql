-- This file is to bootstrap a database for the CS3200 project. 

-- Create a new database.  You can change the name later.  You'll
-- need this name in the FLASK API file(s),  the AppSmith 
-- data source creation.
DROP DATABASE IF EXISTS nubee;
CREATE DATABASE IF NOT EXISTS nubee;

-- Via the Docker Compose file, a special user called webapp will 
-- be created in MySQL. We are going to grant that user 
-- all privilages to the new database we just created. 
-- TODO: If you changed the name of the database above, you need 
-- to change it here too.
grant all privileges on nubee.* to 'webapp'@'%';
flush privileges;

-- Move into the database we just created.
-- TODO: If you changed the name of the database above, you need to
-- change it here too. 
use nubee;

-- Put your DDL 

CREATE TABLE IF NOT EXISTS User
(
    userID int PRIMARY KEY auto_increment,
    userName varchar(28) UNIQUE,
    isAdmin tinyint(1) DEFAULT(0) NOT NULL,
    age int
);

CREATE TABLE IF NOT EXISTS Message
(
    messageID int NOT NULL AUTO_INCREMENT,
    senderID int,
    receiverID int,
    content varchar(255),
    PRIMARY KEY(messageID),
    FOREIGN KEY (senderID) REFERENCES User(userID),
    FOREIGN KEY (receiverID) REFERENCES User(userID),
    INDEX (senderID, receiverID)
);


CREATE TABLE IF NOT EXISTS Report
(
    reporterID int,
    offenderID int,
    reportID int PRIMARY KEY auto_increment,
    content varchar(255),
    FOREIGN KEY (reporterID) REFERENCES User(userID),
    FOREIGN KEY (offenderID) REFERENCES User(userID),
    INDEX (reporterID, offenderID)
);

CREATE TABLE IF NOT EXISTS Project
(
    projectID int PRIMARY KEY auto_increment,
    overview text,
    title varchar(255),
    funding int,
    visibility tinyint(1) DEFAULT(1) NOT NULL,
    createdAt datetime DEFAULT(CURRENT_TIMESTAMP),
    updatedAt datetime ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Role
(
    userID int,
    projectID int,
    role varchar(255),
    FOREIGN KEY(userID) REFERENCES User(userID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(projectID) REFERENCES Project(projectID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (userID, projectID)
);

CREATE TABLE IF NOT EXISTS Post
(
    userID int,
    postID int PRIMARY KEY auto_increment,
    title varchar(255),
    content text,
    createdAt datetime DEFAULT(CURRENT_TIMESTAMP),
    FOREIGN KEY (userID) REFERENCES User(userID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    INDEX (userID)
);

CREATE TABLE IF NOT EXISTS Tag
(
    tagID int PRIMARY KEY auto_increment,
    content varchar(255)
);

CREATE TABLE IF NOT EXISTS ProjectTag
(
    tagID int,
    projectID int,
    FOREIGN KEY (tagID) REFERENCES Tag(tagID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (projectID) REFERENCES Project(projectID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY(tagID, projectID)
);

CREATE TABLE IF NOT EXISTS PostTag
(
    tagID int,
    postID int,
    FOREIGN KEY (tagID) REFERENCES Tag(tagID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (postID) REFERENCES Post(postID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY(tagID, postID)
);

CREATE TABLE IF NOT EXISTS Comment
(
    userID int,
    commentID int PRIMARY KEY auto_increment,
    createdAt datetime DEFAULT (CURRENT_TIMESTAMP),
    content   varchar(255),
    FOREIGN KEY (userID) REFERENCES User(userID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    INDEX (userID)
);

CREATE TABLE IF NOT EXISTS Milestone
(
    userID int,
    projectID int,
    milestoneID int PRIMARY KEY auto_increment,
    completed tinyint(1) DEFAULT(0) NOT NULL,
    dueDate datetime,
    FOREIGN KEY (userID) REFERENCES User(userID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (projectID) REFERENCES Project(projectID)
    ON UPDATE CASCADE ON DELETE CASCADE,
    INDEX (userID, projectID)
);

-- Add sample data. 
INSERT INTO Project
  (overview,title ,funding)
VALUES
  ('this is a sample project', 'moby dick', 5000000);

