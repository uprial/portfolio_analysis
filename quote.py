# vim: ts=4 sts=4 sw=4 et: syntax=python

from datetime import datetime

class Quote(object):
    DATE_FORMAT = "%Y-%m-%d"
    DELIM = ","

    CLOSE_PRICE_KEYS = ["\"closing value\"", "close"]

    def __init__(self, date, close_price):
        self._date = date
        self._close_price = close_price

    @classmethod
    def decode(cls, data):
        date = datetime.strptime(data[cls.get_date_field_name()], cls.DATE_FORMAT)

        close_price_key = None
        for _close_price_key in cls.CLOSE_PRICE_KEYS:
            if _close_price_key in data:
                close_price_key = _close_price_key

        if close_price_key is None:
            raise Exception(("Couldn't find any of close price keys %s in data: %s."
                             % (cls.CLOSE_PRICE_KEYS, data)))

        close_price = (float)(data[close_price_key])

        return Quote(date, close_price)

    @property
    def date(self):
        return self._date

    @property
    def close_price(self):
        return self._close_price

    @classmethod
    def get_date_field_name(cls):
        return "date"

    def get_header(self):
        return self.DELIM.join(["Date", "Close"])

    def __str__(self):
        return self.DELIM.join([self._date.strftime(self.DATE_FORMAT), "%f" % (self._close_price)])

    def __repr__(self):
        return self.__str__()
