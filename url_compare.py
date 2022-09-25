import re
import csv
import requests
import sys
import argparse
from bs4 import BeautifulSoup
import lxml
from lxml.html.clean import clean_html
from tabulate import tabulate

def main():
    url1, url2, ifile, ofile = process_args()
    result = dict()
    if ifile is not None:
        print("process file")
        # check it is a csv file
        result = read_csv_file(ifile)

    else:
        try:
            diff = compare_urls(url1, url2)
            if len(diff) != 0:
                index_key = url1 + ' and ' + url2
                result[index_key] = diff
        except Exception as e:
            sys.exit(e)
    print(result)
    # Output data
    table = list()
    for urls, diff in result.items():
        diff_str = ', '.join(diff)
        table.append([urls, diff_str])

    if ofile is not None:
        header = ["URLs", "Difference"]
        with open(ofile, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write multiple rows
            writer.writerows(table)
    else:
        header = ["URLs", "Difference"]
        print(tabulate(table, headers=header, tablefmt="fancy_grid"))


def compare_urls(url1, url2):
    elements_to_compare = ['title', 'desc']
    result_key = url1 + ' : ' + url2
    try:
        url1_resp = requests.get(url1)
        url2_resp = requests.get(url2)
        difference = list()

        soup1 = BeautifulSoup(url1_resp.text, 'html.parser')
        soup2 = BeautifulSoup(url2_resp.text, 'html.parser')

        for element in elements_to_compare:
            if element == 'desc':
                desc1       = get_page_description(soup1.find_all("meta"))
                desc2       = get_page_description(soup2.find_all("meta"))
                if desc1 != desc2:
                    difference.append(element)
            elif element == 'title':
                title1 = soup1.find('title')
                title2 = soup2.find('title')
                if title1 is not None and title2 is not None and title1.get_text() != title2.get_text():
                    difference.append(element)

    except Exception as e:
        sys.exit(e)

    return difference

def read_csv_file(ifile):
    result = dict()
    with open(ifile) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                url1, url2 = parse_urls(row)
                diff = compare_urls(url1, url2)
                if len(diff) != 0:
                    index_key = url1 + ' and ' + url2
                    result[index_key] = diff
    print(result)
    return result

def parse_urls(row):
    url1 = row['url1']
    url2 = row['url2']
    return url1, url2

def get_page_description(meta_list):
    desc = ""
    for meta in meta_list:
        if meta.get('name') == "description":
            desc = meta.get('content')

    return desc


def process_args():
    parser = argparse.ArgumentParser(description='Compare two URLs content and metadata values',
            prog='url_compare')
    parser.add_argument('-i', '--ifile', nargs='?', help='input filename content list of URls')
    parser.add_argument('-o', '--ofile', nargs='?', help='Filename to output the result')
    parser.add_argument('-l1', '--link1', nargs='?', help="First UrL link")
    parser.add_argument('-l2', '--link2', nargs='?', help='Second URL link')

    try:
        args = parser.parse_args()

        link1 = args.link1
        link2 = args.link2
        ifile = args.ifile
        ofile = args.ofile

        if (link1 is not None or link2 is not None) and ifile is not None:
            raise Exception("Only one of these two can be provided (link1 and link2) or ifile ")
    except argparse.ArgumentError as e:
        sys.exit(e.message())
    except Exception as e:
        sys.exit(str(e))

    url1 = 'link1'
    url2 = 'link2'

    return link1, link2, ifile, ofile


if __name__ == "__main__":
    main()