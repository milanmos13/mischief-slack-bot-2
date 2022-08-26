import os
import requests
from slackclient import SlackClient
from requests.structures import CaseInsensitiveDict


def send_message(msg, channel="#bot-beta-testing", url='', bot_name='Workout-Bot V.1'):
    slack_token = os.getenv('BOT_OAUTH_ACCESS_TOKEN')
    sc = SlackClient(slack_token)
    if url == '':
        sc.api_call("chat.postMessage", channel=channel, text=msg, username=bot_name)
    else:
        sc.api_call("chat.postMessage", channel=channel, text=msg, username=bot_name, icon_url=url)


def send_debug_message(msg, bot_name='im dumb'):
    send_message(msg, channel="#bot-debug", bot_name=bot_name)


def send_tribe_message(msg, channel="#bot-beta-testing", bot_name="Workout-Bot V.1"):
    send_message(msg, channel, bot_name=bot_name)


def send_calendar_message(msg):
    send_message(msg, channel="#bot-beta-testing", bot_name='Workout-Bot V.1')


def get_group_info():
    print("group info called")
    url = "https://slack.com/api/users.list"
    token = os.getenv('BOT_OAUTH_ACCESS_TOKEN')
    auth = {"Authorization" : "Bearer " + token}

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    resp = requests.post(url, headers=headers, data=token).json()
    json = requests.get(url, headers=auth).json()
    print("resp", resp)
    print("json", json)
    return resp


def get_emojis():
    url = 'https://slack.com/api/emoji.list?token=' + os.getenv('OAUTH_ACCESS_TOKEN')
    json = requests.get(url).json()
    return json


def open_im(user_id):
    url = "https://slack.com/api/im.open?token=" + os.getenv('BOT_OAUTH_ACCESS_TOKEN') + "&user=" + user_id
    json = requests.get(url).json()
    return json


def create_poll(channel_id, title, options, ts, anon):
    slack_token = os.getenv('BOT_OAUTH_ACCESS_TOKEN')
    sc = SlackClient(slack_token)
    actions = []
    block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*" + title + "*"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Delete Poll",
                    "emoji": True
                },
                "value": str(ts),
                "action_id": "deletePoll:" + str(ts),
                "style": "danger"
            }
        },
        {
            "type": "divider"
        }
    ]
    for i in range(0, len(options)):
        block.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": options[i]
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Vote",
                    "emoji": True
                },
                "value": str(ts),
                "action_id": "votePoll:" + str(i) + ":" + str(anon)
            }
        })
        block.append({
            "type": "divider"
        })

    block.append({
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "DM me the current results",
                    "emoji": True
                },
                "action_id": "dmPoll:" + str(ts),
                "style": "primary"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Remind the slackers",
                    "emoji": True
                },
                "action_id": "remindPoll:" + str(ts),
                "style": "danger"
            }
        ]

    })
    print(block)
    sc.api_call("chat.postMessage", channel=channel_id, blocks=block)


def send_categories(title, channel_id, categories):
    slack_token = os.getenv('BOT_OAUTH_ACCESS_TOKEN')
    sc = SlackClient(slack_token)
    block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*" + title + "*"
            }
        }
    ]
    for category in categories:
        if len(categories[category]) > 0:
            block.append({"type": "divider"})
            block.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*" + category + "*"
                }
            })
            names = ""
            for i in range(len(categories[category])):
                names += str(i + 1) + ") " + categories[category][i] + "\n"
            block.append({
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": names
                }
            })
        else:
            block.append({"type": "divider"})
            block.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*" + category + "*"
                }
            })
    print(block)
    sc.api_call("chat.postMessage", channel=channel_id, blocks=block)
