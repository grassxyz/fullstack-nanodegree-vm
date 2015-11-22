#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM Matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    deleteMatches()
    c.execute("DELETE FROM Players")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(name) AS totalNum FROM Players")
    numOfPlayers = c.fetchone()[0]
    conn.close()
    return numOfPlayers


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    
    conn = connect()
    c = conn.cursor()
    cleanedName = bleach.clean(name)
    
    c.execute("INSERT INTO Players (name) VALUES (%s) RETURNING id", (cleanedName,))
    id = c.fetchone()[0]
    c.execute("INSERT INTO Matches (id, totalWins, totalMatches) VALUES (%s, %s, %s)", (id, 0, 0))
  
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM PlayerStandings")

    listOfPlayerStanding = c.fetchall()

    conn.close()
    return listOfPlayerStanding

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE Matches SET (totalWins, totalMatches) = (totalWins+1, totalMatches+1) WHERE id = (%s)", (winner,))
    c.execute("UPDATE Matches SET (totalMatches) = (totalMatches+1) WHERE id = (%s)", (loser,))

    conn.commit()
    conn.close()

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    curPlayerStandings = playerStandings()
    swissPairs = []
    for cur in range(0, len(curPlayerStandings)-1,2):
        swissPairs.append((curPlayerStandings[cur][0], curPlayerStandings[cur][1], 
                          curPlayerStandings[cur+1][0], curPlayerStandings[cur+1][1]))

    return swissPairs



