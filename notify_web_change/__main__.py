#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import hashlib
import shelve

from settings import WEB_LIST
from mail import MailServer


def get_website_body(url):
    res_text = requests.get(url).text
    body = BeautifulSoup(res_text, "lxml").body
    return body


def generate_hash(text):
    hash = hashlib.md5()
    hash.update(text.encode("utf-8"))
    return hash.hexdigest()


def _get_store_name(url):
    url = url.replace("https://", "")
    url = url.replace("http://", "")
    url = url.replace("www.", "")
    name = url.replace(".", "_")
    name = name.replace("/", "_")
    return "hash_" + name


def compare_hashes(h1, h2):
    if not h2:
        return "New tracking started.", False
    if h1 == h2:
        return "Unchanged since last check.", False
    return "Changes detected.", True


def main():
    to_notify = []
    with shelve.open('hashes.db') as db:
        for web in WEB_LIST.split(","):
            body = get_website_body(web)
            new_hash = generate_hash(body)
            store_name = _get_store_name(web)
            prev_hash = db.get(store_name)
            res, notify = compare_hashes(new_hash, prev_hash)
            if notify:
                to_notify.append(web)
            print("%s: %s" % (store_name, res))
            # Store new hash:
            db[store_name] = new_hash

    with MailServer() as smtp:
        for website in to_notify:
            smtp.send_notification(website)


if __name__ == "__main__":
    main()
