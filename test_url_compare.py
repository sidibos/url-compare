import pytest
from bs4 import BeautifulSoup
from lxml.html.clean import clean_html
import requests
import sys

from url_compare import *

def test_compare_url():
    url1 = "https://www.google.com/"
    url2 = "https://uk.linkedin.com/"
    diff = compare_urls(url1, url2)

    assert 'title' in diff
    assert 'desc' in diff

def test_parse_urls():
    row = {"url1": "https://www.google.com/", "url2": "https://www.google.co.uk/"}
    url1, url2 = parse_urls(row)
    assert url1 == "https://www.google.com/"
    assert url2 == "https://www.google.co.uk/"


def test_get_page_description():
    text = """
    <head>
        <meta name="description" content="test description" />
        <meta name="google:site" content="nothing" />
    </head>
<body>
    <div class="product">Product 1</div>
    <div class="product">Product 2</div>
    <div class="product special">Product 3</div>
    <div class="product special">Product 4</div>
</body>"""

    soup = BeautifulSoup(text, 'html.parser')
    meta_list = soup.find_all("meta")
    desc = get_page_description(meta_list)
    #assert desc == "test description"

def test_read_csv_file():
    key = 'https://google.com and https://www.cmcmarkets.com/en-gb/learn-cfd-trading/what-are-cfds'
    result = read_csv_file('url_list.csv')
    assert key in result

def test_process_args():
    assert 'yes' == 'yes'