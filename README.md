# Mischief Tracking Bot
A variation of the tribe-workout-bots repo. Done on Render since Heroku removed their free tier for PostGre.

## Deploying on Render

### Pre-Reqs:
1. Make an account on Render
1a. Connect your Github account to Render (alternatively, just deploy with one of our public bot repos)
2. Have your bot repo ready

## Create Web Service 
1. From the Render dashboards, click "New +" at the top and select Web Service
2. Connect your bot repository (or paste the bot repository under Public Git repository)
3. Fill out the following: 
**Name**: Can be whatever you want
**Region**: Probably any of these is fine; I usually go with Oregon/Us-west
**Environment**: Python 3
**Build command**: Might be already filled in; if not go with "pip install -r requirements.txt"
**Run command**: gunicorn app:app
**Instance type**: select the free one
4. "Create web service"

## Create DB
1. From the Render dashboards, click "New +" at the top and select Web Service

## Set up Environment Variables


# DB
Table can be created with:
name 0
num_posts 1
num_workouts 2
num_lifts 3
num_cardio 4
num_sprints 5
num_throws 6
num_regen 7
num_play 8
num_volunteer 9
score 10
date 11
id 12
last time 13
```
CREATE TABLE mischief_data(name text, num_posts SMALLINT, num_workouts SMALLINT, num_lifts SMALLINT, num_cardio SMALLINT, num_sprints SMALLINT, num_throws SMALLINT, num_regen SMALLINT, num_play SMALLINT, num_volunteer SMALLINT, score numeric(4, 1), last_post DATE, slack_id CHAR(11), last_time BIGINT);
```

I never got the DB working automatically because I am lazy. So instead I manually inserted each Slack member's row with the following:
```
INSERT INTO mischief_data VALUES ('<Name>', 0, 0, 0, 0, 0, 0, 0, 0, 0, '2022-11-11','<Slack ID>', 0);
```

# POINTS
```
lift - 2 pts
cardio - 1 pt
sprints - 2 pt
throw - 1 pt
yoga/stretch/regen - 1.5 pts
mini/goalty/tryout - 3 pts
volunteer - 3 pt
```
See app.py, db file to modify, parse additions method in season challenge
