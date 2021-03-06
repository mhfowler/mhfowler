from settings.common import SECRETS_DICT

import datetime
import json
import time
from slackclient import SlackClient

from django.http import HttpResponse


def slack_notify_message(message):
    bot_token = SECRETS_DICT['CITIGROUP_SLACKBOT_TOKEN']
    sc = SlackClient(bot_token)

    general_channel_id = 'C0GEA5C1X'
    sc.api_call('chat.postMessage', channel=general_channel_id,
                text='@channel: {}'.format(message), link_names=1,
                as_user=True)


def citigroup_slack_bot():
    bot_token = SECRETS_DICT['CITIGROUP_SLACKBOT_TOKEN']
    sc = SlackClient(bot_token)

    log_message_window = datetime.timedelta(hours=12)
    oldest_window = datetime.datetime.now() - log_message_window
    oldest_window = time.mktime(oldest_window.timetuple())

    cronbox_channel_id = 'C0KC1FWNA'
    cronbox_messages = sc.api_call('channels.history', channel=cronbox_channel_id, oldest=oldest_window)
    cronbox_messages_dict = json.loads(cronbox_messages)
    found_git_sync = False
    for message in cronbox_messages_dict['messages']:
        if 'synced crontab with git' in message['text']:
            found_git_sync = True

    warnings_channel_id = 'C0KCAG7AL'
    if not found_git_sync:
        sc.api_call('chat.postMessage', channel=warnings_channel_id,
                    text='@channel: did not find message with "synced crontab with git" '
                         'in channel #cronbox. '
                         'This suggests that cronbox is not syncing its crontab with git. ', link_names=1)
    else:
        sc.api_call('chat.postMessage', channel=warnings_channel_id,
                    text='k')


def citigroup_slackbot_endpoint(request):
    citigroup_slack_bot()
    return HttpResponse('citigroup slackbot processed')


if __name__ == '__main__':
    slack_notify_message('hmmmm ? hmmm')