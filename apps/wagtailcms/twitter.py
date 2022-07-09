import re

import tweepy
from django.conf import settings
from django.core.cache import cache


class TwitterTimeline:
    KEY = "twitter/twitter/timeline"
    KEY_LT = "twitter/twitter/timeline_longterm"
    KEY_US = "twitter/twitter/username"

    def __init__(self, count=0, cache_timeout=600, cache_long_term_timeout=86400):
        if count == 0:
            count = settings.TWITTER_DEFAULT_COUNT
        self.count = count
        self.cache_timeout = cache_timeout
        self.cache_long_term_timeout = cache_long_term_timeout

        self.re_url = re.compile(r"([A-Za-z]+://[A-Za-z\d-_]+\.[A-Za-z\d-_:%&~?/.=]+)")
        self.re_url_sub = r'<a href="\g<1>">\g<1></a>'
        self.re_hashtag = re.compile(r"#+(?P<hashtag>[A-Za-z\d-_]+)")
        self.re_hashtag_sub = (
            r'<a href="https://twitter.com/search/%23\g<hashtag>">#\g<hashtag></a>'
        )
        self.re_username = re.compile(r"@+(?P<username>[A-Za-z\d-_]+)")
        self.re_username_sub = (
            r'<a href="https://twitter.com/\g<username>">@\g<username></a>'
        )

    @staticmethod
    def connect():
        tset = getattr(settings, "TWITTER_TIMELINE", None)
        if tset:
            auth = tweepy.OAuth2AppHandler(
                tset["consumer_key"], tset["consumer_secret"]
            )
            # auth.set_access_token(tset["access_token"], tset["access_token_secret"])
            return tweepy.API(auth)
        raise Exception("NO TWITTER_TIMELINE in django settings.py")

    def linkify(self, tweet: str) -> str:
        tweet = self.re_url.sub(self.re_url_sub, tweet)
        tweet = self.re_hashtag.sub(self.re_hashtag_sub, tweet)
        tweet = self.re_username.sub(self.re_username_sub, tweet)
        tweet = re.sub("\r\n|\r|\n", "<br />", tweet)
        return tweet

    def extract_tweets(self, timeline):
        stati = []
        for status in timeline:  # tweepy.Status
            update = {}

            if getattr(status, "retweeted_status", None):
                status = status.retweeted_status

            update["id"] = status.id
            # update["id_str"] = status.user.id_str
            update["screen_name"] = status.user.screen_name
            update["name"] = status.user.name
            update["profile_image_url_https"] = status.user.profile_image_url_https
            update["created_at"] = status.created_at
            update["text"] = self.linkify(status.text)

            if getattr(status, "quoted_status", None):
                update["quoted_status"] = {}
                update["quoted_status"]["text"] = self.linkify(
                    status.quoted_status.text
                )
                try:
                    media = status.quoted_status.extended_entities["media"][0][
                        "media_url_https"
                    ]
                    update["quoted_status"]["media_url_https"] = media
                except:
                    pass
            if getattr(status, "extended_entities", None):
                try:
                    update["extended_entities"] = {
                        "media_url_https": status.extended_entities["media"][0][
                            "media_url_https"
                        ]
                    }
                except KeyError:
                    pass

            rt = getattr(status, "retweeted_status", None)
            if rt:
                update[
                    "deep_link"
                ] = f"https://twitter.com/{rt.user.screen_name}/status/{rt.id}"
            else:
                update[
                    "deep_link"
                ] = f"https://twitter.com/{status.user.screen_name}/status/{status.id}"

            stati.append(update)
        return stati

    def get_timeline(self, username=None):
        if username is None:
            username = settings.TWITTER_DEFAULT_USERNAME
        result = cache.get(self.KEY)
        cached_username = cache.get(self.KEY_US)
        if not result or cached_username != username:
            try:
                api = self.connect()
                timeline = api.user_timeline(screen_name=username, count=self.count)
                result = self.extract_tweets(timeline)
                cache.set(self.KEY, result, self.cache_timeout)
                cache.set(self.KEY_LT, result, self.cache_long_term_timeout)
                cache.set(self.KEY_US, username)
            except:
                result = cache.get(self.KEY_LT)
                if not result:
                    result = ""
        return result


if __name__ == "__main__":
    import environ

    BASE_DIR = environ.Path(__file__) - 4
    env = environ.Env()
    env.read_env(BASE_DIR(".env"))
    settings.configure(
        TWITTER_TIMELINE=(
            {
                "consumer_key": env("DJANGO_TWITTER_CONSUMER_KEY"),
                "consumer_secret": env("DJANGO_TWITTER_CONSUMER_SECRET"),
                "access_token": env("DJANGO_TWITTER_ACCESS_TOKEN"),
                "access_token_secret": env("DJANGO_TWITTER_ACCESS_TOKEN_SECRET"),
            }
            if env("DJANGO_TWITTER_CONSUMER_KEY", default="")
            else None
        )
    )
    cache.clear()
    print(TwitterTimeline(count=10).get_timeline("LM_Africa"))
