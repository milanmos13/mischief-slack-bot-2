import os
import urllib.parse
import urllib.request
import psycopg2

from psycopg2 import sql
from slack_api import *

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)
__token__ = os.getenv('BOT_OAUTH_ACCESS_TOKEN')
__auth__ = {"Authorization" : "Bearer " + __token__}

#CREATE TABLE mischief_data(name text, num_posts SMALLINT, num_workouts SMALLINT, num_red SMALLINT, num_white SMALLINT, num_black SMALLINT, num_throw SMALLINT, num_regen SMALLINT, num_altitude SMALLINT, score numeric(4, 1), last_post DATE, slack_id CHAR(9), last_time BIGINT, pod text, team text)

# this doesn't really work
def init_db(member_info):
    print("ATTEMPTING INIT WITH: ", member_info)
    try:
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        cursor = conn.cursor()
        if cursor.rowcount == 0 and channel_id == "C03UHTL3J58":
            for member in member_info['members']:   
                cursor.execute(sql.SQL("INSERT INTO mischief_data VALUES (%s, 0, 0, 0, 0, 0, 0, 0, 0, 0, now(), %s, %s)"),
                               [member['real_name'], member['id'], now()])
            send_debug_message("%s is new to Mischief" % name)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        send_debug_message(error)
        return False

def add_num_posts(mention_id, event_time, name, channel_id):
    try:
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        cursor = conn.cursor()
        cursor.execute(sql.SQL(
            "UPDATE mischief_data SET num_posts=num_posts+1 WHERE slack_id = %s"),
            [mention_id[0]])
        if cursor.rowcount == 0 and channel_id == "C03UHTL3J58":
            cursor.execute(sql.SQL("INSERT INTO mischief_data VALUES (%s, 0, 0, 0, 0, 0, 0, 0, 0, 0, now(), %s, %s, %s, %s)"),
                           [name, mention_id[0], event_time, name, name])
            send_debug_message("%s is new to Mischief" % name)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        send_debug_message(error)
        return True

def collect_stats(datafield, rev):
    try:
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        cursor = conn.cursor()
        # get all of the people whose scores are greater than -1 (any non players have a workout score of -1)
        cursor.execute(sql.SQL(
            "SELECT * FROM mischief_data WHERE score > -1.0"), )
        leaderboard = cursor.fetchall()
        leaderboard.sort(key=lambda s: s[9], reverse=rev)  # sort the leaderboard by score descending
        string1 = "Leaderboard:\n"
        for x in range(0, len(leaderboard)):
            string1 += '%d) %s on Team %s (Pod %s) with %.1f point(s); %.1d red; %.1d white; %.1d black; %.1d throw(s); %.1d regen; %.1d altitude training. \n' % (x + 1, leaderboard[x][0], 
                leaderboard[x][14], leaderboard[x][13], leaderboard[x][9], leaderboard[x][3], leaderboard[x][4], leaderboard[x][5],
                leaderboard[x][6], leaderboard[x][7], leaderboard[x][8])
        cursor.close()
        conn.close()
        return string1
    except (Exception, psycopg2.DatabaseError) as error:
        send_debug_message(error)

def get_group_info():
    url = "https://slack.com/api/users.list"
    json = requests.get(url, headers=__auth__).json()
    return json


def get_emojis():
    url = 'https://slack.com/api/emoji.list'
    json = requests.get(url, headers=__auth__).json()
    return json


def add_to_db(channel_id, names, addition, red_num, white_num, black_num, throw_num, regen_num, altitude_num, num_workouts, ids):  # add "addition" to each of the "names" in the db
    send_debug_message("atitude num: " + altitude_num)
    cursor = None
    conn = None
    num_committed = 0
    try:
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        print("names: ", names)
        print("ids: ", ids)
        cursor = conn.cursor()
        for x in range(0, len(names)):
            print("starting", names[x])
            cursor.execute(sql.SQL(
                "SELECT score FROM mischief_data WHERE slack_id = %s"), [str(ids[x])])
            score = cursor.fetchall()[0][0]
            score = int(score)
            if score != -1:
                cursor.execute(sql.SQL("""
                    UPDATE mischief_data SET num_workouts=num_workouts+%s,
                    num_red=num_red+%s, num_white=num_white+%s, num_black=num_black+%s, num_throw=num_throw+%s, 
                    num_regen=num_regen+%s, num_altitude=num_altitude+%s,
                    score=score+%s, last_post=now() WHERE slack_id = %s
                    """),
                    [str(num_workouts), str(red_num), str(white_num), str(black_num), str(throw_num), str(regen_num), str(altitude_num), str(addition), ids[x]])
                conn.commit()
                send_debug_message("committed %s with %s points" % (names[x], str(addition)))
                print("committed %s" % names[x])
                num_committed += 1
            else:
                send_debug_message("invalid workout poster found " + names[x])
    except (Exception, psycopg2.DatabaseError) as error:
        send_debug_message(str(error))
    finally:
        if cursor is not None:
            cursor.close()
            conn.close()
        return num_committed


def get_mental_req(mention_id):
    cursor = None
    conn = None
    req_string = ""
    try:
        urllib.parse.uses_netloc.append("postgres")
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        cursor = conn.cursor()
        cursor.execute(sql.SQL(
            "SELECT * FROM mischief_data WHERE slack_id = %s"), [mention_id[0]])
        entry = cursor.fetchall()
        req_string += '%s requirements fulfilled: %.1d red; %.1d black; %.1d white.' % (entry[x][0], entry[x][3], entry[x][4], entry[x][5])
        cursor.close()
        conn.close()
        return req_string
    except (Exception, psycopg2.DatabaseError) as error:
        send_debug_message(error)


def subtract_from_db(names, subtraction, ids):  # subtract "subtraction" from each of the "names" in the db
    cursor = None
    conn = None
    num_committed = 0
    try:
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        cursor = conn.cursor()
        for x in range(0, len(names)):
            cursor.execute(sql.SQL(
                "UPDATE mischief_data SET score = score - %s WHERE slack_id = %s"),
                [subtraction, ids[x]])
            conn.commit()
            send_debug_message("subtracted %s" % names[x])
            num_committed += 1
    except (Exception, psycopg2.DatabaseError) as error:
        send_debug_message(str(error))
    finally:
        if cursor is not None:
            cursor.close()
            conn.close()
        return num_committed


def reset_scores():  # reset the scores of everyone
    cursor = None
    conn = None
    try:
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        cursor = conn.cursor()
        cursor.execute(sql.SQL("""
            UPDATE mischief_data SET num_workouts = 0, num_red = 0, num_white = 0, num_black = 0, num_throw = 0, 
            num_regen = 0, num_altitude = 0, score = 0, last_post = now() WHERE score != -1
        """))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        send_debug_message(str(error))
    finally:
        if cursor is not None:
            cursor.close()
            conn.close()


def reset_talkative():  # reset the num_posts of everyone
    cursor = None
    conn = None
    try:
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        cursor = conn.cursor()
        cursor.execute(sql.SQL(
            "UPDATE mischief_data SET num_posts = 0 WHERE workout_score != -1"))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        send_debug_message(str(error))
    finally:
        if cursor is not None:
            cursor.close()
            conn.close()

def add_workout(name, slack_id, workout_type):
    cursor = None
    conn = None
    try:
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    except (Exception, psycopg2.DatabaseError) as error:
        send_debug_message(str(error))
    finally:
        if cursor is not None:
            cursor.close()
            conn.close()

def get_workouts_after_date(date, type, slack_id):
    cursor = None
    conn = None
    workouts = []
    try:
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    except (Exception, psycopg2.DatabaseError) as error:
        send_debug_message(str(error))
    finally:
        if cursor is not None:
            cursor.close()
            conn.close()
    return workouts

def get_group_workouts_after_date(date, type):
    cursor = None
    conn = None
    workouts = []
    print(date, type)
    try:
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    except (Exception, psycopg2.DatabaseError) as error:
        send_debug_message(str(error))
    finally:
        if cursor is not None:
            cursor.close()
            conn.close()
    return workouts
