from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from googl import Googl
from tweet.models import TweetedObject
from twitter.api import Twitter
from twitter.oauth import OAuth
from django.contrib.contenttypes.models import ContentType

CONSUMER_KEY = '5r75gsq8W59Ik3BHfnYYuw'
CONSUMER_SECRET = 'xoVDPK59kscew67NYLe8Yw8FToaUhDYBP3Yj6fKwE'
TWITTER_LENGTH = getattr(settings, 'TWITTER_LENGTH', 140)

def register(instance):
    if getattr(settings, 'TWEET_SAVED', True):
        post_save.connect(receiver=tweet, sender=instance)

def tweet(sender, instance, **kwargs):
    if not hasattr(instance, 'may_tweet') or instance.may_tweet():
        t = SavedNotification(instance)
        t.tweet()

class SavedNotification(object):
    def __init__(self, sender_instance):
        self.sender_instance = sender_instance
        self.sender_type = ContentType.objects.get_for_model(self.sender_instance.__class__)

        self.url = "http://%s%s" % (Site.objects.get_current(), self.sender_instance.get_absolute_url())
        self.msg = self.sender_instance.twitter_message if hasattr(self.sender_instance, 'twitter_message') else str(self.sender_instance)
        self.googl = Googl(getattr(settings, 'GOOGL_KEY', None))
        self.auth = OAuth(settings.TWEET_SAVED_OAUTH_TOKEN, settings.TWEET_SAVED_OAUTH_TOKEN_SECRET,
                          CONSUMER_KEY,
                          CONSUMER_SECRET,
        )
        self.twitter = Twitter(auth=self.auth)

    def tweet(self):
        if not TweetedObject.objects.filter(content_type=self.sender_type, object_id=self.sender_instance.pk).exists():
            url = self.googl.shorten(self.url)['id']
            max_message_length = TWITTER_LENGTH - (len(url) + 1)
            message = "%s %s" % (self.msg[:max_message_length], url)
            response = self.twitter.statuses.update(status=message)
            print response
            self._remember_tweet(response)

    def _remember_tweet(self, response):
        t = TweetedObject(status_id=response['id'], content_object=self.sender_instance, screen_name=response['user']['screen_name'])
        t.save()

