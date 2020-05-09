#! /usr/bin/env python
# vim: ts=4 sts=4 sw=4 et: syntax=python

import sys
from datetime import datetime

from quote import Quote
from quote_history import QuoteHistory

if len(sys.argv) < 2:
    print >> sys.stderr, "%s NAME" % (sys.argv[0])
    exit(1)

NAME = sys.argv[1]

LEVERAGE = 3.0
TER = 0.0095

def report(quote, leveraged_price):
    print >> sys.stderr, "%s, %f" % (quote, leveraged_price)


def get_expenses(prev_date, curr_date):
    days_in_year = (datetime(curr_date.year, 12, 31) - datetime(curr_date.year, 1, 1)).days + 1
    daily_ter = (1.0 + TER) ** (1.0 / days_in_year) - 1.0
    days_passed = (curr_date - prev_date).days
    expenses = (1.0 + daily_ter) ** days_passed - 1.0
    return expenses


def get_leverage(open_price, close_price, expenses):
    return (1 + LEVERAGE * (close_price - open_price) / open_price) * (1 - expenses)


# Leveraged ETFs use futures, so pay no dividends,
# please refer to https://www.quora.com/Do-leveraged-ETFs-such-as-UPRO-reinvest-stock-dividends
def main():
    quotes = QuoteHistory("%s.csv" % (NAME)).get_quotes(Quote)
    quote0 = quotes[0]

    leveraged_price = quote0.close_price

    report(quote0, leveraged_price)

    l_quotes = []
    for quote in quotes:
        expenses = get_expenses(quote0.date, quote.date)
        leveraged_price *= get_leverage(quote0.close_price, quote.close_price, expenses)

        l_quote = Quote(quote.date, leveraged_price)
        l_quotes.append(l_quote)
        quote0 = quote

    QuoteHistory("%s-x%0.1f-%0.2f%%.csv" % (NAME, LEVERAGE, TER * 100)).put_quotes(l_quotes)

    report(quote0, leveraged_price)

main()
