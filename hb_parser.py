import HTMLParser
import csv
import sys
import os
import argparse

class HBParser(HTMLParser):
    DEFAULT_OUTPUT_NAME = 'output.csv'
    FORMAT_TAG_1 = 'subproduct-selector'
    FORMAT_TAG_2 = 'selector-content'    
    FORMAT_TAG_3 = 'text-holder'
    DATA_TAG_1 = 'h2'
    DATA_TAG_2 = 'p'

    def __init__(filename: str=''):
        super.__init__()
        if filename:
            self.filename = filename
        else:
            print(f"Invalid filename: {filename}. Exiting.")
            exit()

        # handle command-line args



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

    if len(args) > 2:
        hbp.write(args[2])
    else:
        print(f"No output filename. Writing to default file: {os.path.join(
            os.getcwd(), hbp.DEFAULT_OUTPUT_NAME)}")
        hbp.write()


# subproduct-selector
# selector-content
# text-holder

# data in h2
# data in p