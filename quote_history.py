#! /usr/bin/env python
# vim: ts=4 sts=4 sw=4 et: syntax=python

class QuoteHistory(object):
    NEW_LINE = "\n"
    DELIM = ","

    def __init__(self, filename):
        self.filename = filename

    def get_quotes(self, quotes_class):
        with open(self.filename, "r") as filehandle:
            data = filehandle.read()

        lines = data.split(self.NEW_LINE)
        keys = None

        i = 0
        while i < len(lines):
            cells = self._split(lines[i])
            i += 1

            if cells[0].lower() == quotes_class.get_date_field_name():
                keys = []
                for cell in cells:
                    keys.append(cell.lower())
                break

        if keys is None:
            raise Exception(("Couldn't find a header with '%s' column."
                             % (quotes_class.get_date_field_name())))

        quotes = []
        while i < len(lines):
            if lines[i]:
                cells = self._split(lines[i])
                data = {}
                null = True
                for j in xrange(len(keys)):
                    data[keys[j]] = cells[j]
                    if keys[j] != quotes_class.get_date_field_name() and cells[j].lower() != "null":
                        null = False

                if not null:
                    quotes.append(quotes_class.decode(data))
            i += 1

        if len(quotes) < 1:
            raise Exception("Couldn't find quotes.")

        return quotes

    def put_quotes(self, quotes):
        with open(self.filename, "w+") as filehandle:
            # filehandle = sys.stdout
            filehandle.write(quotes[0].get_header() + self.NEW_LINE)
            for quote in quotes:
                filehandle.write(quote.__str__() + self.NEW_LINE)


    @classmethod
    def _split(cls, line):
        return line.strip().split(cls.DELIM)
