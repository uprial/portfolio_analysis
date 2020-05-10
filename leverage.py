#! /usr/bin/env python
# vim: ts=4 sts=4 sw=4 et: syntax=python

import sys
from datetime import datetime

from quote import Quote
from dividend_quote import DividendQuote
from quote_history import QuoteHistory

if len(sys.argv) < 2:
    print >> sys.stderr, "%s NAME" % (sys.argv[0])
    exit(1)

class BaseQuote(Quote):

    def __init__(self, date, price):
        super(BaseQuote, self).__init__(date, price)
        self._original_price = price

    @property
    def original_price(self):
        return self._original_price

    @original_price.setter
    def original_price(self, original_price):
        self._original_price = original_price

    def __str__(self):
        return self.DELIM.join([self._date.strftime(self.DATE_FORMAT),
                                "%f" % (self._price),
                                "%f" % (self._original_price)])

NAME = sys.argv[1]

LEVERAGE = 3.0
TER = 0.0095
BASE_TER = 0.002
STOCKS = 0.5605
BONDS = 0.1845

def report(quote, leveraged_price):
    print >> sys.stderr, "%s,%f" % (quote, leveraged_price)

def get_exp_agregate(annual_rate, prev_date, curr_date):
    days_in_year = (datetime(curr_date.year, 12, 31) - datetime(curr_date.year, 1, 1)).days + 1
    daily_rate = (1.0 + annual_rate) ** (1.0 / days_in_year) - 1.0
    days_passed = (curr_date - prev_date).days
    return (1.0 + daily_rate) ** days_passed - 1.0

def get_expenses(prev_date, curr_date):
    return get_exp_agregate(TER, prev_date, curr_date)

def get_leverage(open_price, close_price, expenses):
    return (1 + LEVERAGE * (close_price - open_price) / open_price) * (1 - expenses)


# Leveraged ETFs use futures, so pay no dividends, please refer to
# https://www.proshares.com/media/prospectus/tqqq_summary_prospectus.pdf?param=1589022358703
def main():
    quotes = QuoteHistory("%s.csv" % (NAME)).get_quotes(BaseQuote)
    d_quotes = QuoteHistory("%s_dividends.csv" % (NAME)).get_quotes(DividendQuote)
    b_quotes = QuoteHistory("%s_^IRX.csv" % (NAME)).get_quotes(Quote)

    prev_quote = quotes[0]
    prev_bill_date = prev_quote.date

    leveraged_price = prev_quote.price
    leveraged_price = 1.730208

    report(prev_quote, leveraged_price)

    for i in xrange(len(quotes)):
        exp_agregate = get_exp_agregate(BASE_TER, prev_quote.date, quotes[i].date)
        quotes[i].original_price = quotes[i].price * (1.0 + exp_agregate)

    dividends = {}
    for quote in d_quotes[1:]:
        dividends[quote.date] = quote.price


    bills = {}
    for quote in b_quotes[1:]:
        bills[quote.date] = quote.price / 100

    l_quotes = []
    for quote in quotes[1:]:
        expenses = get_expenses(prev_quote.date, quote.date)
        leveraged_price *= get_leverage(prev_quote.original_price, quote.original_price, expenses)

        if quote.date in dividends:
            leveraged_price *= 1.0 + dividends[quote.date] / quote.price * STOCKS
            del dividends[quote.date]

        if quote.date in bills:
            exp_agregate = get_exp_agregate(bills[quote.date], prev_bill_date, quote.date)
            leveraged_price *= 1.0 + exp_agregate * BONDS
            prev_bill_date = quote.date
            del bills[quote.date]

        l_quote = Quote(quote.date, leveraged_price)
        l_quotes.append(l_quote)
        prev_quote = quote

    if dividends:
        raise Exception("Excessive dividends data: %s" % (dividends))

    if bills:
        raise Exception("Excessive bills data: %s" % (bills))

    QuoteHistory("%s-x%0.1f-%0.2f%%.csv" % (NAME, LEVERAGE, TER * 100)).put_quotes(l_quotes)

    report(prev_quote, leveraged_price)

main()
