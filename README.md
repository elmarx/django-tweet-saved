tweet-saved
===========

What does it do?
----------------

Tweet if a model has been saved. Useful to announce news, blogposts, etc.


How does it work?
-----------------

- notification via django service
- shortens url with googl (via *python-googl*)
- uses package *twitter* to tweet the notification
- remember that an instance has been tweeted (via djangos contentype/generic
  foreign keys), so notifications are only sent once

Prerequisites
-------------

I developed and tested this app (only) using Python 2.6 and Django trunk (1.3-beta atm).

If I did the setup.py correctly, *python-googl* and *twitter* should get
installed with this package.

How to use it
-------------

1. Install, add *tweet* to your ``INSTALLED_APPS``.

2. get the *oauth* token/secret and add it to your *settings.py*:
    <pre><code>
    $ ./manage.py tweet_oauth
    Hi there! We're gonna get you all set up to use tweet_saved.

    In the web browser window that opens please choose to Allow
    access. Copy the PIN number that appears on the next page and paste or
    type it here:

    Please enter the PIN: 1234567
    Please add
    TWEET_SAVED_OAUTH_TOKEN = 'xxxxxxxxx'
    TWEET_SAVED_OAUTH_TOKEN_SECRET = 'xxxx'
    to your settings.py
    </code></pre>

3. Register your model
    <pre><code>

    ...
    from tweet import tweeter

    class MyModel(models.model):
        ...

    tweeter.register(MyModel)
    </pre></code>

4. if not present, add a [method get_absolute_url](http://docs.djangoproject.com/en/dev/ref/models/instances/#get-absolute-url
 "Django documentation on get-absolute-url")
 to your model.

5. recommended steps (but not required):
    Add a property ``twitter_message`` to your model to define the message to tweet.
    This message will automatically shrinked to fit into the 140 character limit.

    If this method is not defined, the object is simply converted to string.

    This is the ``twitter_message`` of my object, augmented with hashtags
    (using the tags from django-tagging)
    <pre><code>
    @property
    def twitter_message(self):
        reo = re.compile('(%s)' % '|'.join([x.name for x in self.tag_objects]), flags=re.IGNORECASE)
        return 'Blog: ' + re.sub(reo, '#\g<1>', self.headline)
    </pre></code>

    Add a method ``may_tweet`` returning a bool, if you want to delay the tweet,
    i.e. wait until the object is marked as public.

    Example:
    <pre>
    <code>
    def may_tweet(self):
        return self.published is not None and self.published.date() < datetime.date.today()
    </code>
    </pre>

    6. If you want to keep track of the shortened urls, get a Google/Googl key,
    and add it to your *settings.py*

    ``GOOGL_KEY = 'xxxx'``

TODO
----

- add tests
- document the code
- add an option to tweet "saved" multiple times

Forks
-----

If you fork the code (according to create a new project/app), please remember
to change the CONSUMER_KEY and the CONSUMER_SECRET.

Features/Bugs/Fixes/Suggestions
-------------------------------

For anything like the above, contact me/send pull requests, etc.