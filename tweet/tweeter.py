from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from googl import Googl
from twitter.api import Twitter
from twitter.oauth import OAuth

CONSUMER_KEY = '5r75gsq8W59Ik3BHfnYYuw'
CONSUMER_SECRET = 'xoVDPK59kscew67NYLe8Yw8FToaUhDYBP3Yj6fKwE'
TWITTER_LENGTH = getattr(settings, 'TWITTER_LENGTH', 140)

def tweet(sender, instance, **kwargs):
    t = SavedNotification(instance)
    t.tweet()

class SavedNotification(object):
    def __init__(self, sender):
        self.url = "http://%s%s" % (Site.objects.get_current(), sender.get_absolute_url())
        self.msg = sender.twitter_message if hasattr(sender, 'twitter_message') else str(sender)
        self.googl = Googl(getattr(settings, 'GOOGL_KEY', None))
        self.auth = OAuth(settings.TWEET_SAVED_OAUTH_TOKEN, settings.TWEET_SAVED_OAUTH_TOKEN_SECRET,
                          CONSUMER_KEY,
                          CONSUMER_SECRET,
        )
        self.twitter = Twitter(auth=self.auth)

    def tweet(self):
        url = self.googl.shorten(self.url)['id']
        max_message_length = TWITTER_LENGTH - (len(url) + 1)
        message = "%s %s" % (self.msg[:max_message_length], url)
        response = self.twitter.statuses.update(status=message)
        # todo: save to db and remember not to tweet this item again.

class ServiceSetup(object):

    def register(self, instance):
        post_save.connect(receiver=tweet, sender=instance)

tweeter = ServiceSetup()