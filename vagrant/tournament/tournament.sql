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

CREATE TABLE Players ( name TEXT NOT NULL,
                       id SERIAL PRIMARY KEY,
                       total_wins INTEGER DEFAULT 0,
                       total_matches INTEGER DEFAULT 0);

-- created as required by code review

CREATE TABLE Matches ( match_id SERIAL PRIMARY KEY,
                       winner_id INTEGER REFERENCES Players(id) ON DELETE CASCADE,
                       loser_id INTEGER REFERENCES Players(id) ON DELETE CASCADE);

