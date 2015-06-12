import praw
import time
import pickle
import re
import os
import sys
import argparse
import requests
import urllib.request
from random import randint
from pprint import pprint
from google import search
from lxml import html
from lxml import etree


def ffn_make_from_requests(requests):
    links = ffn_link_finder(requests)
    found_ffn = ffn_comment_maker(links)
    return found_ffn


def ffn_link_finder(fic_names):
    links_found = []
    for fic_name in fic_names:

        # Obfuscation.
        time.sleep(randint(1, 3))
        sleep_milliseconds = randint(500, 3000)
        time.sleep(sleep_milliseconds / 1000)

        search_request = 'site:fanfiction.net/s/ ' + fic_name
        print("SEARCHING: ", search_request)

        search_results = search(search_request, num=1, stop=1)
        link_found = next(search_results)
        links_found.append(link_found)
        print("FOUND: " + link_found)

    return links_found


def ffn_comment_maker(links):
    comment = ''
    for link in links:
        comment += '{0}\n&nbsp;\n\n'.format(ffn_description_maker(link))
    return comment


def ffn_description_maker(link):
    current = Story(link)
    decoded_title = current.title.decode('ascii', errors='replace')
    decoded_author = current.author.decode('ascii', errors='replace')
    decoded_summary = current.summary.decode('ascii', errors='replace')
    decoded_data = current.data.decode('ascii', errors='replace')

    print("Making a description for " + decoded_title)

    # More pythonic string formatting.
    header = '[***{0}***]({1}) by [*{2}*]({3})'.format(decoded_title,
                                                       link, decoded_author, current.authorlink)

    formatted_description = '{0}\n\n>{1}\n\n>{2}\n\n'.format(
        header, decoded_summary, decoded_data)
    # print("Description for " + decoded_title + ": \n" + formatted_description)
    print(formatted_description)
    return formatted_description


class Story:

    def __init__(self, url):
        self.url = url
        self.raw_data = []

        self.title = ""
        self.author = ""
        self.authorlink = ""
        self.summary = ""
        self.data = ""

        self.parse_html(url)
        self.encode()

    def parse_html(self, url):
        page = requests.get(self.url)
        tree = html.fromstring(page.text)

        self.title = (tree.xpath('//*[@id="profile_top"]/b/text()'))[0]
        self.summary = (tree.xpath('//*[@id="profile_top"]/div/text()'))[0]
        self.author += (tree.xpath('//*[@id="profile_top"]/a[1]/text()'))[0]
        self.authorlink = 'https://www.fanfiction.net' + \
            tree.xpath('//*[@id="profile_top"]/a[1]/@href')[0]

        # Getting the metadata was a bit more tedious.
        self.raw_data += (tree.xpath('//*[@id="profile_top"]/span[4]/a[1]/text()'))
        self.raw_data += (tree.xpath('//*[@id="profile_top"]/span[4]/text()[2]'))
        self.raw_data += (tree.xpath('//*[@id="profile_top"]/span[4]/a[2]/text()'))
        self.raw_data += (tree.xpath('//*[@id="profile_top"]/span[4]/text()[3]'))
        self.raw_data += (tree.xpath('//*[@id="profile_top"]/span[4]/span[1]/text()'))
        self.raw_data += (tree.xpath('//*[@id="profile_top"]/span[4]/text()[4]/text()'))
        self.raw_data += (tree.xpath('//*[@id="profile_top"]/span[4]/span[2]/text()'))
        self.raw_data += (tree.xpath('//*[@id="profile_top"]/span[4]/text()[5]'))

    def encode(self):
        self.title = self.title.encode('ascii', errors='replace')
        self.author = self.author.encode('ascii', errors='replace')
        self.summary = self.summary.encode('ascii', errors='replace')
        self.data = self.data.encode('ascii', errors='replace')
        for string in self.raw_data:
            self.data += string.encode('ascii', errors='replace')

# # DEBUG
# x = Story('https://www.fanfiction.net/s/8303194/1/Magics-of-the-Arcane')
# print(x.authorlink)
# print(x.title)
# print(x.author)
# print(x.summary)
# print(x.data)
