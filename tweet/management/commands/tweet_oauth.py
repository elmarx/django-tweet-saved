from django.core.management.base import BaseCommand
import tweet.tweeter
from twitter.oauth_dance import oauth_dance

class Command(BaseCommand):
    help = "Help you to generate the twitter oauth token."

    def handle(self, *args, **options):
        (oauth_token, oauth_token_secret) = oauth_dance('tweet_saved', tweet.tweeter.CONSUMER_KEY, tweet.tweeter.CONSUMER_SECRET)
        self.stdout.write(
            "Please add\n"
            "TWEET_SAVED_OAUTH_TOKEN = '%s'\n"
            "TWEET_SAVED_OAUTH_TOKEN_SECRET = '%s'\n"
            "to your settings.py\n" % (oauth_token, oauth_token_secret)
        )