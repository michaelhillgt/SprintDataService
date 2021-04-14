CREATE TABLE IF NOT EXISTS team_members(
  user_id text,
  name text,
  team text,
  PRIMARY KEY ( team, user_id )  
  );

CREATE TABLE IF NOT EXISTS sprint_stars(
  team text,
  sprint_date text,
  user_id text,  
  category text,
  PRIMARY KEY (team, sprint_date, user_id )
  );

CREATE TABLE IF NOT EXISTS story_points(
  team text,
  user_id text, 
  issue_id text, 
  story_points text,
  PRIMARY KEY (team, user_id, issue_id )
  ) WITH default_time_to_live = 120;

CREATE TABLE IF NOT EXISTS test_tickets(
  team text,
  user_id text, 
  worklog_id text, 
  time_spent text,
  PRIMARY KEY ( team, user_id, worklog_id ) 
  ) WITH default_time_to_live = 120;

CREATE TABLE IF NOT EXISTS code_quality(
  team text,
  user_id text, 
  worklog_id text, 
  time_spent text,
  PRIMARY KEY ( team, user_id, worklog_id ) 
  ) WITH default_time_to_live = 120;
    
CREATE TABLE IF NOT EXISTS assists(
  team text,
  user_id text, 
  worklog_id text, 
  time_spent text,
  PRIMARY KEY ( team, user_id, worklog_id ) 
  ) WITH default_time_to_live=120;

CREATE TABLE IF NOT EXISTS kudos(
  team text,
  user_id text, 
  worklog_id text,
  recipient_id text,
  PRIMARY KEY ( team, user_id, worklog_id ),
  ) WITH default_time_to_live=120;