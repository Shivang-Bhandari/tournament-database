#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    dbConnect = connect()
    dbCursor = dbConnect.cursor()
    dbCursor.execute("delete from matchData;")
    dbConnect.commit()
    dbConnect.close()

def deletePlayers():
    """Remove all the player records from the database."""
    dbConnect = connect()
    dbCursor = dbConnect.cursor()
    dbCursor.execute("delete from playerData;")
    dbConnect.commit()
    dbConnect.close()

def countPlayers():
    """Returns the number of players currently registered."""
    dbConnect = connect()
    dbCursor = dbConnect.cursor()
    results = dbCursor.fetchall(dbCursor.execute("select countt(*) form playerData;"))
    return results[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    dbConnect = connect()
    dbCursor = dbConnect.cursor()
    dbCursor.execute("INSERT into playerData (name) values(%s)", (name,);)
    dbConnect.commit()
    dbConnect.close()


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
    dbConnect = connect()
    dbCursor = dcConnect.cursor()
    query = """
    create view playerStandingData as
    select playerData.ID,playerData.name,
        (select count(matchData.winnerID) from matchData where playerData.ID = matchData.winnderID) as winn,
        (select count(matchData.matchID) from matchData where playerData.ID = matchData.winnerID OR playerData.ID = matchData.loserID) as games
    from playerData
    order by winn desc, games desc;
    select * from playerStandingData;

    """

    dbCursor.execute(query)
    results = dbCursor.fetchall()
    dbConnect.close()

    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    dbConnect = connect()
    dbCursor = dbConnect.cursor()
    dbCursor.execute("INSERT into matchData (winnerID, loserID) values (%s, %s)" (winner,loser) )

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
    playerStandingDataset = playerStandings()
    pear=[]

    for i in range(0,len(a),2):
        j=(playerStandingDataset[i][0],playerStandingDataset[i][1],playerStandingDataset[i+1][0],playerStandingDataset[i+1][1])
        pear.append(j)

    return pear
