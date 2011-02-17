from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

class TweetedObject(models.Model):
    status_id = models.BigIntegerField(unique=True)
    screen_name = models.CharField(max_length=20)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%(model_url)s, http://twitter.com/#!/%(screen_name)s/status/%(id)s" % \
        {'model_url': self.content_object.get_absolute_url(), 'screen_name': self.screen_name,
         'id': str(self.status_id)}
