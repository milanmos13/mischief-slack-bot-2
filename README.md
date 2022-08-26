# Mischief Tracking Bot
A variation of the tribe-workout-bots repo. Setup can found in that [README](https://github.com/samloop/tribe-workout-bots/blob/master/README.md).

# DB
Table can be created with:
name 0
num_post 1
num_workout 2
num_red 3
num_white 4
num_black 5
num_throw 6
num_regen 7
num_altitude 8
score 9
date 10
id 11
last time 12
pod 13
team 14
```
CREATE TABLE mischief_data(name text, num_posts SMALLINT, num_workouts SMALLINT, num_red SMALLINT, num_white SMALLINT, num_black SMALLINT, num_throw SMALLINT, num_regen SMALLINT, num_altitude SMALLINT, score numeric(4, 1), last_post DATE, slack_id CHAR(11), last_time BIGINT, pod text, team text);
```

I never got the DB working automatically because I am lazy. So instead I manually inserted each Slack member's row with the following:
```
INSERT INTO mischief_data VALUES ('<Name>', 0, 0, 0, 0, 0, 0, 0, 0, 0, '2022-11-11','<Slack ID>', 0, '<pod>', '<team>');
```

# POINTS

    WHITE_POINTS = 1.0
    RED_POINTS = 1.0
    BLACK_POINTS = 0.5
    THROW_POINTS = 1.0
    REGEN_POINTS = 2.0
    ALTITUDE_POINTS = 0.0

See app.py, db file to modify, parse additions method in season challenge
