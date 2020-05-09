# vim: ts=4 sts=4 sw=4 et: syntax=python

from datetime import datetime

class Quote(object):
    DATE_FORMAT = "%Y-%m-%d"
    DELIM = ","

    PRICE_KEYS = ["\"closing value\"", "close"]

    def __init__(self, date, price):
        self._date = date
        self._price = price

    @classmethod
    def decode(cls, data):
        date = datetime.strptime(data[cls.get_date_field_name()], cls.DATE_FORMAT)

        price_key = None
        for _price_key in cls.PRICE_KEYS:
            if _price_key in data:
                price_key = _price_key

        if price_key is None:
            raise Exception(("Couldn't find any of price keys %s in data: %s."
                             % (cls.PRICE_KEYS, data)))

        price = (float)(data[price_key])

        return Quote(date, price)

    @property
    def date(self):
        return self._date

    @property
    def price(self):
        return self._price

    @classmethod
    def get_date_field_name(cls):
        return "date"

    def get_header(self):
        return self.DELIM.join(["Date", "Close"])

    def __str__(self):
        return self.DELIM.join([self._date.strftime(self.DATE_FORMAT), "%f" % (self._price)])

    def __repr__(self):
        return self.__str__()
