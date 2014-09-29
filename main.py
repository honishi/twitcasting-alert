#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.config
import configparser
import threading
import tcalert


CONFIG_FILE = os.path.dirname(os.path.abspath(__file__)) + '/main.configuration'


# main sequence
def main():
    logging.config.fileConfig(CONFIG_FILE)

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    (polling_interval, user_configs) = load_configuration(config)
    log_configuration(polling_interval, user_configs)

    monitor_threads = open_monitor_threads(polling_interval, user_configs)
    wait_monitor_ends(monitor_threads)


# internal methods
def load_configuration(config):
    user_configs = []
    section = 'twitcasting'

    polling_interval = float(config[section]['polling_interval'])
    target_users = config[section]['target_users'].split(',')

    for target_user in target_users:
        message = config[target_user]['message']
        consumer_key = config[target_user]['consumer_key']
        consumer_secret = config[target_user]['consumer_secret']
        access_key = config[target_user]['access_key']
        access_secret = config[target_user]['access_secret']

        user_config = {
            'target_user': target_user,
            'message': message,
            'consumer_key': consumer_key,
            'consumer_secret': consumer_secret,
            'access_key': access_key,
            'access_secret': access_secret}

        user_configs.append(user_config)

    return (polling_interval, user_configs)


def log_configuration(polling_interval, user_configs):
    logging.debug("polling_interval:{}".format(polling_interval))

    for user_config in user_configs:
        logging.debug("user:{} message:{} ck:{} cs:{} ak:{} as:{}"
                      .format(user_config['target_user'], user_config['message'],
                              user_config['consumer_key'], user_config['consumer_secret'],
                              user_config['access_key'], user_config['access_secret']))


def open_monitor_threads(polling_interval, user_configs):
    monitor_threads = []

    for user_config in user_configs:
        monitor_thread = threading.Thread(
            name="{}".format(user_config['target_user']),
            target=tcalert.monitor,
            args=(user_config['target_user'], user_config['message'],
                  user_config['consumer_key'], user_config['consumer_secret'],
                  user_config['access_key'], user_config['access_secret'],
                  polling_interval))
        monitor_thread.start()
        monitor_threads.append(monitor_thread)

    return monitor_threads


def wait_monitor_ends(monitor_threads):
    for monitor_thread in monitor_threads:
        monitor_thread.join()


# application entry point
if __name__ == "__main__":
    main()
