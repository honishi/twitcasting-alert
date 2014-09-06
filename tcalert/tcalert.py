__author__ = 'honishi'

import logging
import urllib.request
import urllib.parse
import json
import datetime
import time
from twython import Twython


TWITCASTING_API_LIVE_STATUS = 'http://api.twitcasting.tv/api/livestatus'
TWITCASTING_LIVE_URL = 'http://twitcasting.tv/'


def monitor(target_user, message, consumer_key, consumer_secret, access_key, access_secret,
            polling_interval=3):
    logging.debug("started monitoring...")

    last_is_live = None

    while True:
        try:
            response = query_twitcasting(target_user)
            is_live = response["islive"]

            if last_is_live is None:
                pass
            elif last_is_live is False and is_live is True:
                logging.info("detected live.")
                tweet(target_user, message,
                      consumer_key, consumer_secret, access_key, access_secret)

            last_is_live = is_live

        except Exception as error:
            logging.error("caught exception in polling loop, error: [{}]".format(error))
            # os.sys.exit()

        time.sleep(polling_interval)

    logging.debug("finished monitoring.")


def query_twitcasting(target_user):
    url = TWITCASTING_API_LIVE_STATUS + '?type=json&user=' + target_user

    request = urllib.request.urlopen(url)
    encoding = request.headers.get_content_charset()
    response = request.read().decode(encoding)
    logging.debug(response)

    parsed = json.loads(response)
    logging.debug(parsed)

    return parsed


def tweet(target_user, message, consumer_key, consumer_secret, access_key, access_secret):
    status = "{} {} ({})".format(message, TWITCASTING_LIVE_URL + target_user,
                                 datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

    try:
        twitter = Twython(consumer_key, consumer_secret, access_key, access_secret)
        twitter.update_status(status=status)
    except Exception as error:
        logging.error("caught exception in tweet:{}".format(error))
