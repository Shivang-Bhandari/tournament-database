-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE playerData (
  ID serial primary key,
  name text
);

CREATE TABLE matchData (
  matchID serial primary key,
  winnerID int references playerData(ID),
  loserID int references playerData(ID)
);
