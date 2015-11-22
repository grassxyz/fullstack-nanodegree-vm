#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=tournament")
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error in establishing database connection")


def deleteMatches():
    """Remove all the match records from the database."""
    conn, c = connect()
    c.execute("DELETE FROM Matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, c = connect()
    c.execute("DELETE FROM Players")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn, c = connect()
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
    
    conn, c = connect()
    cleanedName = bleach.clean(name)
    
    c.execute("INSERT INTO Players (name) VALUES (%s)", (cleanedName,))

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
    conn, c = connect()
    c.execute("SELECT id, name, total_wins, total_matches FROM Players ORDER BY total_wins DESC")

    listOfPlayerStanding = c.fetchall()

    conn.close()
    return listOfPlayerStanding

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, c = connect()
    c.execute("INSERT INTO Matches (winner_id, loser_id) VALUES (%s, %s)", (winner, loser))
    c.execute("UPDATE Players SET (total_wins, total_matches) = (total_wins+1, total_matches+1) "
              "WHERE id = (%s)", (winner,))
    c.execute("UPDATE Players SET (total_matches) = (total_matches+1) WHERE id = (%s)", (loser,))
    
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
    

    '''
    check if odd number, if so, top winner skip next pairings
    '''


    if len(curPlayerStandings)%2== 0:
        startPos = 0    
    else:
        startPos = 1

    for cur in range(startPos, len(curPlayerStandings)-1,2):
        swissPairs.append((curPlayerStandings[cur][0], curPlayerStandings[cur][1], 
                          curPlayerStandings[cur+1][0], curPlayerStandings[cur+1][1]))


    return swissPairs



