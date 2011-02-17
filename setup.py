import exceptions

try:
    from setuptools import setup
except exceptions.ImportError:
    from distutils.core import setup


setup(name="django-tweet-saved",
      author="Elmar Athmer",
      author_email="elmar@nixus-minimax.de",
      url="https://github.com/zauberpony/django-tweet-saved",
      version='0.8.1',
      packages=['tweet', 'tweet.migrations', 'tweet.management', 'tweet.management.commands'],
      install_requires=[
              'twitter',
              'python-googl'
      ],
      description="post an update to twitter if a model changed in django",
      classifiers=[
              "Programming Language :: Python",
              "License :: OSI Approved :: BSD License",
              "Operating System :: OS Independent",
              "Development Status :: 4 - Beta",
              "Intended Audience :: Developers",
              ]
)
