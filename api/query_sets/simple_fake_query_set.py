__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class SimpleFakeQuerySet:
    def __init__(self, get_data):
        self.get_data = get_data
