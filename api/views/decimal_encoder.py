import decimal
import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
