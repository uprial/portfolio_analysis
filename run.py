#! /usr/bin/env python
# vim: ts=4 sts=4 sw=4 et: syntax=python

import sys

from quote import Quote
from quote_history import QuoteHistory

if len(sys.argv) < 6:
    print >> sys.stderr, "%s TAX SHARE1 NAME1 SHARE2 NAME2" % (sys.argv[0])
    exit(1)

TAX = (float)(sys.argv[1])
SHARE1 = (float)(sys.argv[2])
NAME1 = sys.argv[3]
SHARE2 = (float)(sys.argv[4])
NAME2 = sys.argv[5]

SAVINGS = 100.0

def balance(amount1, price1, share1, amount2, price2, share2, tax): # pylint: disable=too-many-arguments
    total_amount = amount1 * price1 + amount2 * price2 + SAVINGS
    t_amount1 = total_amount * share1 / price1
    t_amount2 = total_amount * share2 / price2
    excessive_money = SAVINGS
    if (t_amount1 > amount1) and (excessive_money > 0):
        inc = min(excessive_money, (t_amount1 - amount1) * price1)
        amount1 = amount1 + inc / price1
        excessive_money = excessive_money - inc

    if (t_amount2 > amount2) and (excessive_money > 0):
        inc = min(excessive_money, (t_amount2 - amount2) * price2)
        amount2 = amount2 + inc / price2
        excessive_money = excessive_money - inc

    if excessive_money > 0.0001:
        raise Exception("Some money has not been spent on the portfolio: %f" % (excessive_money))

    if tax > 0.0001:
        if amount1 < t_amount1 - 0.001:
            inc = (amount2 - t_amount2) * price2 * (1.0 - tax)
            amount1 = amount1 + inc / price1
            amount2 = t_amount2

        if amount2 < t_amount2 - 0.001:
            inc = (amount1 - t_amount1) * price1 * (1.0 - tax)
            amount2 = amount2 + inc / price2
            amount1 = t_amount1

    return amount1, amount2

def main():
    quotes1 = QuoteHistory("%s.csv" % (NAME1)).get_quotes(Quote)
    quotes2 = QuoteHistory("%s.csv" % (NAME2)).get_quotes(Quote)

    amount1 = 0.0
    amount2 = 0.0

    r_quotes = []
    prev_year = None
    for i in xrange(len(quotes1)):
        quote1 = quotes1[i]
        quote2 = quotes2[i]

        if (prev_year is None) or (quote1.date.year > prev_year):
            prev_year = quote1.date.year

            amount1, amount2 = balance(amount1, quote1.price, SHARE1,
                                       amount2, quote2.price, SHARE2,
                                       TAX)


        r_quote = Quote(quote1.date, amount1 * quote1.price + amount2 * quote2.price)
        r_quotes.append(r_quote)

    QuoteHistory(("%.2f-%s-%.2f-%s-tax-%.0f.csv"
                  % (SHARE1, NAME1, SHARE2, NAME2, TAX * 100))).put_quotes(r_quotes)

    print >> sys.stderr, ("%f x %f = %f"
                          % (amount1, quote1.price, amount1 * quote1.price))
    print >> sys.stderr, ("%f x %f = %f"
                          % (amount2, quote2.price, amount2 * quote2.price))

main()
