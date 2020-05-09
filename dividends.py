#! /usr/bin/env python
# vim: ts=4 sts=4 sw=4 et: syntax=python

import sys
from datetime import datetime

from quote import Quote
from quote_history import QuoteHistory

class DividendQuote(Quote):
    PRICE_KEYS = ["dividends"]

if len(sys.argv) < 2:
    print >> sys.stderr, "%s NAME" % (sys.argv[0])
    exit(1)

NAME = sys.argv[1]

def main():
    quotes = QuoteHistory("%s.csv" % (NAME)).get_quotes(Quote)
    dividends = QuoteHistory("%s_dividends.csv" % (NAME)).get_quotes(DividendQuote)

    prices = {}
    for quote in quotes:
        prices[quote.date] = quote.price

    d_stats = {}
    for d_quote in dividends:

        year = d_quote.date.year
        if not year in d_stats:
            d_stats[year] = {
                "count": 0,
                "amount": 0.0,
                "percent": 0.0
            }

        d_stats[year]["count"] += 1
        d_stats[year]["amount"] += d_quote.price
        d_stats[year]["percent"] += d_quote.price / prices[d_quote.date]

    d_max = 0.0
    d_sum = 0.0
    d_num = 0

    banned_years = [min(d_stats.keys()), datetime.today().year]
    for year, data in d_stats.iteritems():
        print "%d\t%d\t%f\t%f%%" % (year, data["count"], data["amount"], data["percent"])
        if year not in banned_years:
            d_num += 1
            d_sum += data["percent"]
            d_max = max(d_max, data["percent"])


    print "%s annual dividends: %f%% avg, %f%% max" % (NAME, 100.0 * d_sum / d_num, 100.0 * d_max)
main()
