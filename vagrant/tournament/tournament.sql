-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- drop the existing tournament database if existed
DROP DATABASE IF EXISTS tournament;


-- create database tournament and then connect to it
CREATE DATABASE tournament;

\c tournament

-- create database tables

CREATE TABLE Players ( name TEXT,
                       id SERIAL PRIMARY KEY);


CREATE TABLE Matches (id SERIAL REFERENCES Players (id),
                      totalWins INTEGER,
                      totalMatches INTEGER);

-- create a commonly used view

CREATE VIEW PlayerStandings AS
    SELECT a.id, a.name, b.totalWins, b.totalMatches
    FROM Players as a, Matches as b
    WHERE a.id = b.id ORDER BY totalWins DESC;

