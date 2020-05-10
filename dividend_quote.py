# vim: ts=4 sts=4 sw=4 et: syntax=python

from quote import Quote

class DividendQuote(Quote):
    PRICE_KEYS = ["dividends"]
