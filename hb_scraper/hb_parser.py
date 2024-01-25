from html.parser import HTMLParser
import csv
import sys
import os
import argparse

"""
IMPORTED PACKAGE DOCUMENTATION
https://docs.python.org/3/library/html.parser.html
https://docs.python.org/3/library/csv.html
"""

# bundle the records together
class Record:
    def __init__(self, title: str='', publisher='', title_first: bool=True):
        self.title = title
        self.publisher = publisher
        self.title_first = title_first

    def get_dict(self):
        return {'title': self.title,
                'publisher': self.publisher}

    def get_tuple(self, title_first: bool=True):
        if title_first or self.title_first:
            return self.title, self.publisher
        return self.publisher, self.title

    def display(self, title_first: bool=True):
        if title_first or self.title_first:
            return f"{self.title}: {self.publisher}"
        return f"{self.publisher}: {self.title}"

class HBParser(HTMLParser):
    DEFAULT_OUTPUT_NAME = 'output.csv'
    FORMAT_TAG_1 = 'subproduct-selector'
    FORMAT_TAG_2 = 'selector-content'    
    FORMAT_TAG_3 = 'text-holder'
    DATA_TAG_1 = 'h2'
    DATA_TAG_2 = 'p'
    COLUMNS = ['Title', 'Publisher']

    def __init__(self, filename: str='', output_filename: str=DEFAULT_OUTPUT_NAME):
        super().__init__()
        if filename:
            self.filename = filename
        else:
            print(f"Invalid filename: {filename}. Exiting.")
            exit()

        # navigation flags
        self.in_format_1 = False
        self.in_format_2 = False
        self.in_format_3 = False
        self.in_data_1 = False
        self.in_data_2 = False

        # key data structure
        self.records = []
        self.current_record = None

        # data management
        self.output_filename = output_filename

    # entering the tags
    def handle_starttag(self, tag, attrs):
        if attrs and tag != self.DATA_TAG_1:
            name = attrs[0][1]
        else:
            name = tag
        match name:
            case self.FORMAT_TAG_1:
                self.in_format_1 = True
            case self.FORMAT_TAG_2:
                if self.in_format_1:
                    self.in_format_2 = True
            case self.FORMAT_TAG_3:
                if self.in_format_2:
                    self.in_format_3 = True
            case self.DATA_TAG_1:
                if self.in_format_3:
                    self.in_data_1 = True
            case self.DATA_TAG_2:
                if self.in_format_3:
                    self.in_data_2 = True
            case _:
                pass

    # handle data
    def handle_data(self, data):
        if not data:
            return
        if self.in_data_1 and not self.in_data_2:
            self.current_record = Record(title=data)
            self.in_data_1 = False
        elif not self.in_data_1 and self.in_data_2:
            self.current_record.publisher = data
            self.records.append(self.current_record)
            self.current_record = None
            self.in_format_1 = self.in_format_2 = self.in_format_3 = self.in_data_1 = self.in_data_2 = False


    # closes out of the relevant tags
    def handle_endtag(self, tag):
        if tag == self.DATA_TAG_2:
            self.in_format_1 = self.in_format_2 = self.in_format_3 = self.in_data_1 = self.in_data_2 = False

    # display records
    def display_records(self):
        print(len(self.records))
        output = '\n'.join([record.display() for record in self.records])
        return output

    # parse the records
    def parse(self):
        html_str = ''
        with open(self.filename, 'r') as file:
            html_str += file.read()
        self.feed(html_str)

    # write to csv
    def to_csv(self, output_filename: str=''):
        output_filename = output_filename if output_filename else self.output_filename

        with open(output_filename, 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.COLUMNS)
            [writer.writerow([record.title, record.publisher]) for record in self.records]




class ArgParser(argparse.ArgumentParser):
    def __init__(description: str=''):
        super.__init__(description)



if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        filename = args[1]
    else:
        print("Filename required")
        exit()

    hbp = HBParser(filename)
    hbp.parse()
    print(hbp.display_records())
    if len(args) > 2:
        hbp.to_csv(args[2])
    else:
        hbp.to_csv()


# subproduct-selector
# selector-content
# text-holder

# data in h2
# data in p