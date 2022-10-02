from bs4 import BeautifulSoup
import requests
from urllib import parse as urllib_parse
import os
from queue import Queue


class SimpleCounter:
    def __init__(self):
        self.id = 0

    def get_id(self):
        self.id = self.id + 1
        return self.id - 1


def get_page(url):
    req = requests.get(url)
    return req.text


def write_text_to_file(id, text, path_to_folder="data"):
    if not os.path.isdir(path_to_folder):
        os.makedirs(path_to_folder)
    with open(os.path.join(path_to_folder, str(id) + ".html"), "w", encoding="utf-8") as file:
        file.write(text)


def add_url_to_file(id, url, path_to_file="urls.txt"):
    with open(path_to_file, "a", encoding="utf-8") as file:
        file.write(str(id) + ":" + url + "\n")


def add_list_to_queue(queue_, list_):
    for item in list_:
        queue_.put(item)


def parse(url, counter):
    id = counter.get_id()
    page_text = get_page(url)
    add_url_to_file(id, url)
    write_text_to_file(id, page_text)

    soup = BeautifulSoup(page_text, 'html.parser')
    new_links = []
    for link in soup.find_all('a'):
        new_links.append(urllib_parse.urljoin(url, link.get('href')))
    return new_links


def parse_all(init_url, counter, cnt):
    exit = 0
    url_queue = Queue()
    url_queue.put(init_url)
    while not url_queue.empty() and exit < cnt:
        url = url_queue.get()
        add_list_to_queue(url_queue, parse(url, counter))
        exit += 1

def main():
    url = "https://2ch.hk/"
    cnt = 10
    my_counter = SimpleCounter()
    open("urls.txt", "w")  # clear file
    parse_all(url, my_counter, cnt)


main()
