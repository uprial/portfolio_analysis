#! /usr/bin/env python
# vim: ts=4 sts=4 sw=4 et: syntax=python

import sys

from quote import Quote
from quote_history import QuoteHistory

if len(sys.argv) < 2:
    print >> sys.stderr, "%s NAME" % (sys.argv[0])
    exit(1)

NAME = sys.argv[1]

SAVINGS = 100.0

def main():
    quotes = QuoteHistory("%s.csv" % (NAME)).get_quotes(Quote)

    amount = 0.0

    r_quotes = []
    prev_year = None
    for quote in quotes:

        if (prev_year is None) or (quote.date.year > prev_year):
            prev_year = quote.date.year

            amount += SAVINGS / quote.price


        r_quote = Quote(quote.date, amount * quote.price)
        r_quotes.append(r_quote)

    QuoteHistory("%s-%d.csv" % (NAME, SAVINGS)).put_quotes(r_quotes)

    print >> sys.stderr, ("%f x %f = %f"
                          % (amount, quote.price, amount * quote.price))

main()
