from distutils.core import setup

setup(name='tweet_saved',
        version='0.1',
        packages=['tweet'],
        install_requires=[
                'twitter',
                'python-googl'
        ],
        )
