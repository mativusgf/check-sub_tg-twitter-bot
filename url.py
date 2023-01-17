import tweepy
import config

client = tweepy.Client(bearer_token=config.BEARER_TOKEN)

users = client.get_users_followers(id=config.USER_ID)

screen_name = input()

for user in users.data:
    if screen_name in user.username:
        print("Found!")
    else:
        print("Not found!")
