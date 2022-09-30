# Mischief Tracking Bot
A variation of the tribe-workout-bots repo. Setup can found in that [README](https://github.com/samloop/tribe-workout-bots/blob/master/README.md).

# DB
Table can be created with:
name 0
num_posts 1
num_workouts 2
num_lifts 3
num_cardio 4
num_throws 5
num_regen 6
num_play 7
num_compete 8
num_halloween 9
num_soup 10
score 11
date 12
id 13
last time 14
```
CREATE TABLE mischief_data(name text, num_posts SMALLINT, num_workouts SMALLINT, num_lifts SMALLINT, num_cardio SMALLINT, num_throws SMALLINT, num_regen SMALLINT, num_play SMALLINT, num_compete SMALLINT, num_halloween SMALLINT, num_soup SMALLINT, score numeric(4, 1), last_post DATE, slack_id CHAR(11), last_time BIGINT);
```

I never got the DB working automatically because I am lazy. So instead I manually inserted each Slack member's row with the following:
```
INSERT INTO mischief_data VALUES ('<Name>', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2022-11-11','<Slack ID>', 0);
```

# POINTS
```
lift - 2 pts
cardio - 1 pt
throw - 1 pt
yoga/stretch/regen - 1.5 pts
mini/goalty/tryout - 3 pts
competing in something non-frisbee - 3pts
celebrating halloween in some way - 2pts
soup - 1 pt
```
See app.py, db file to modify, parse additions method in season challenge
