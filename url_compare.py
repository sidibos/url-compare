
import re
import requests
import sys
import argparse
from bs4 import BeautifulSoup
import lxml
from lxml.html.clean import clean_html

def main():
    url1, url2, ifile = process_args()
    #resp = requests.get("https://google.com")
    if ifile != None:
        print("process file")
    else:
        try:
            #url1_resp = requests.get(url1)
            #link1_headersJSON = url1_resp.headers
            #url2_resp = requests.get(url2)
            #link2_headersJSON = url2_resp.headers

            #link1_html_text = url1_resp.text
            #link2_html_text = url2_resp.text

            #soup1 = BeautifulSoup(link1_html_text, 'html.parser')
            #soup2 = BeautifulSoup(link2_html_text, 'html.parser')

            #cleantext = re.sub("<.*?>", "", soup1.title)
            result = compare_urls(url1, url2)
           
            
        except Exception as e:
            sys.exit(e)


def compare_urls(url1, url2):
    result = list()
    try:
        url1_resp = requests.get(url1)
        url2_resp = requests.get(url2)

        soup1 = BeautifulSoup(url1_resp.text, 'html.parser')
        soup2 = BeautifulSoup(url2_resp.text, 'html.parser')

        desc1       = get_page_description(soup1.find_all("meta"))
        desc2       = get_page_description(soup2.find_all("meta"))

        print(f"Desc one: {desc1}")
        print(f"desc two: {desc2}")

        #print(soup2.find_all("meta"))
        # print(soup1)
        # print(soup2)

        if soup1.title.string != soup2.title.string:
            print("titles are different", soup1.title.string, soup2.title.string, sep=", ")
        else:
            print("titles are the same", soup1.title.string, soup2.title.string, sep=", ")

    except Exception as e:
        sys.exit(e)
    
    return result

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

        if (link1 != None or link2 != None) and ifile != None:
            raise Exception("Only one of these two can be provided (link1 and link2) or ifile ")
    except argparse.ArgumentError as e:
        sys.exit(e.message())
    except Exception as e:
        sys.exit(str(e))

    url1 = 'link1'
    url2 = 'link2'

    return link1, link2, ifile



if __name__ == "__main__":
    main()