from html.parser import HTMLParser
import csv
import sys
import os
import argparse

# bundle the records together
class Record:
    def __init__(title: str='', publisher='', title_first: bool=True):
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

    def __init__(self, filename: str=''):
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

    # entering the tags
    def handle_starttag(self, tag, attrs):
        match tag:
            case self.FORMAT_TAG_1:
                self.in_format_1 = True
            case self.FORMAT_TAG_2:
                if self.in_format_2:
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
        if self.in_data_1:
            self.current_record = Record(title=data)
        if self.in_data_2:
            self.current_record.publisher = data
            self.records.append(self.current_record)
            self.current_record = None


    # closes out of the relevant tags
    def handle_endtag(self, tag):
        match tag:
            case self.FORMAT_TAG_1:
                self.in_format_1 = False
            case self.FORMAT_TAG_2:
                if self.in_format_2:
                    self.in_format_2 = False
            case self.FORMAT_TAG_3:
                if self.in_format_2:
                    self.in_format_3 = False
            case self.DATA_TAG_1:
                if self.in_format_3:
                    self.in_data_1 = False
            case self.DATA_TAG_2:
                if self.in_format_3:
                    self.in_data_2 = False
            case _:
                pass

    # display records
    def display_records(self):
        output = '\n'.join([record.display() for record in self.records])
        return output

    # parse the records
    def parse(self):
        html_str = ''
        with open(self.filename, 'r') as file:
            html_str += file.read()
        self.feed(html_str)




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
    hbp.display_records()

    # if len(args) > 2:
    #     hbp.write(args[2])
    # else:
    #     print(f"No output filename. Writing to default file: {os.path.join(
    #         os.getcwd(), hbp.DEFAULT_OUTPUT_NAME)}")
    #     hbp.write()


# subproduct-selector
# selector-content
# text-holder

# data in h2
# data in p