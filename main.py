#!/usr/bin/env python3
# NAME: Mastopy
# AUTHOR: Melon Bread
# INFO: Just playing with the Mastodon.py API,
#       and hopefully give it a okay QT UI
#       down the road.
# URL: {INSERT GIT REPO HERE}

import configparser
import os.path
import sys

from mastodon import Mastodon


def main():
    # Load configuration
    instance_url = load_config("Instance_URL")

    # Create application if it does not exist
    if not os.path.isfile("Mastopy_client-cred.secret"):
        create_application(instance_url)

    # Login to Mastodon instance
    mastodon_api = login(instance_url)

    # Make a toot
    keep_on_tooting = True
    while keep_on_tooting:
        make_toot(mastodon_api)

    pass


def load_config(config_setting):
    try:
        config = configparser.ConfigParser()
        config.read("Mastopy.cfg")
        return config["Mastodon"][config_setting]
    except:
        print("ERROR: Mastodon.cfg is missing, corrupt, or formatted incorrectly!")
        sys.exit(1)
    pass


def create_application(url):
    print("Application not created, creating now...")

    if Mastodon.create_app("Mastopy",
                           to_file="Mastopy_client-cred.secret",
                           scopes=['read', 'write'],
                           api_base_url=url):
        print("Application created!")
    else:
        print("Failed to create application!")
        sys.exit(1)

    pass


def login(url):
    if not os.path.isfile("Mastopy_user-cred.secret"):
        print("Please enter your login information below.")
        user_login = input("E-Mail: ")
        user_password = input("Password: ")
        print("Attempting to create login....")
        try:
            mastodon_api = Mastodon(
                client_id="Mastopy_client-cred.secret",
                api_base_url=url
            )
            mastodon_api.log_in(
                username=user_login,
                password=user_password,
                scopes=['read', 'write'],
                to_file="Mastopy_user-cred.secret"
            )
        except:
            print("ERROR: First Login Failed!")
        print("Login made successfully!")
    return Mastodon(
        client_id="Mastopy_client-cred.secret",
        access_token="Mastopy_user-cred.secret",
        ratelimit_method="wait",
        api_base_url=url
    )


def make_toot(mastodon):
    toot_message = input("Please enter your toot ('!EXIT' to quit): ")
    if toot_message == "!EXIT":
        print("See ya next time~")
        sys.exit(0)
    else:
        mastodon.toot(toot_message)
    pass


if __name__ == '__main__':
    sys.exit(main())
