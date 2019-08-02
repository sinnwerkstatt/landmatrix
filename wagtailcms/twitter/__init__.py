import re

import tweepy
from django.conf import settings
from django.core.cache import cache


class TwitterTimeline:
    KEY = 'twitter/twitter/timeline'
    KEY_LT = 'twitter/twitter/timeline_longterm'
    KEY_US = 'twitter/twitter/username'

    def __init__(self, count=20, cache_timeout=600, cache_long_term_timeout=86400):
        self.count = count
        self.cache_timeout = cache_timeout
        self.cache_long_term_timeout = cache_long_term_timeout

        self.re_url = re.compile('([A-Za-z]+:\/\/[A-Za-z0-9-_]+\.[A-Za-z0-9-_:%&~\?\/.=]+)')
        self.re_url_sub = '<a href="\g<1>">\g<1></a>'
        self.re_hashtag = re.compile('#+(?P<hashtag>[A-Za-z0-9-_]+)')
        self.re_hashtag_sub = '<a href="https://twitter.com/search/%23\g<hashtag>">#\g<hashtag></a>'
        self.re_username = re.compile('@+(?P<username>[A-Za-z0-9-_]+)')
        self.re_username_sub = '<a href="https://twitter.com/\g<username>">@\g<username></a>'

    def connect(self):
        tset = getattr(settings, 'TWITTER_TIMELINE', None)
        if tset:
            auth = tweepy.OAuthHandler(tset['consumer_key'], tset['consumer_secret'])
            auth.set_access_token(tset['access_token'], tset['access_token_secret'])
            return tweepy.API(auth)
        raise Exception("NO TWITTER_TIMELINE in django settings.py")

    def linkify(self, tweet: str) -> str:
        tweet = self.re_url.sub(self.re_url_sub, tweet)
        tweet = self.re_hashtag.sub(self.re_hashtag_sub, tweet)
        tweet = self.re_username.sub(self.re_username_sub, tweet)
        tweet = re.sub('\r\n|\r|\n', '<br />', tweet)
        return tweet

    def extract_tweets(self, timeline):
        stati = []
        for status in timeline:
            update = {}

            if getattr(status, 'retweeted_status', None):
                status = status.retweeted_status

            update['id_str'] = status.user.id_str
            update['screen_name'] = status.user.screen_name
            update['name'] = status.user.name
            update['profile_image_url_https'] = status.user.profile_image_url_https
            update['created_at'] = status.created_at
            update['text'] = self.linkify(status.text)

            if getattr(status, 'quoted_status', None):
                update['quoted_status'] = {}
                update['quoted_status']['text'] = self.linkify(status.quoted_status['text'])
                try:
                    media = status.quoted_status['extended_entities']['media'][0]['media_url_https']
                    update['quoted_status']['media_url_https'] = media
                except:
                    pass
            if getattr(status, 'extended_entities', None):
                try:
                    update['extended_entities'] = {
                        'media_url_https': status.extended_entities['media'][0]['media_url_https']
                    }
                except KeyError:
                    pass
            stati.append(update)
        return stati

    def get_timeline(self, username):

        result = cache.get(self.KEY)
        cached_username = cache.get(self.KEY_US)
        if not result or cached_username != username:
            try:
                api = self.connect()
                timeline = api.user_timeline(username, count=self.count)
                result = self.extract_tweets(timeline)
                cache.set(self.KEY, result, self.cache_timeout)
                cache.set(self.KEY_LT, result, self.cache_long_term_timeout)
                cache.set(self.KEY_US, username)
            except:
                result = cache.get(self.KEY_LT)
                if not result:
                    result = ''
        return result


if __name__ == '__main__':
    TwitterTimeline().get_timeline('Twitter')