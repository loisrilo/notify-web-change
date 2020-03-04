#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import hashlib
import shelve
from datetime import datetime
import difflib

from settings import WEB_LIST, THRESHOLD
from mail import MailServer


def get_website_body(url):
    res_text = requests.get(url).text
    body = BeautifulSoup(res_text, "lxml").body
    return body


def generate_hash(text):
    hash = hashlib.md5()
    hash.update(text.encode("utf-8"))
    return hash.hexdigest()


def _get_store_names(url):
    url = url.replace("https://", "")
    url = url.replace("http://", "")
    url = url.replace("www.", "")
    name = url.replace(".", "_")
    name = name.replace("/", "_")
    return "hash_" + name, "body_" + name


def compare_hashes(h1, h2):
    if not h2:
        return "New tracking started.", False
    if h1 == h2:
        return "Unchanged since last check.", False
    return "Changes detected.", True


def compare_bodies(old, new):
    res = ""
    for diff in difflib.Differ().compare(
            str(old).split("\\n"), str(new).split("\\n")):
        if diff[0] in ["+", "-", "?"]:
            res += diff + "\n"
    return res


def main():
    to_notify = []
    with shelve.open('hashes.db') as db:
        for web in WEB_LIST.split(","):
            body = get_website_body(web)
            new_hash = generate_hash(body)
            hash_name, body_name = _get_store_names(web)
            prev_hash = db.get(hash_name)
            res, notify = compare_hashes(new_hash, prev_hash)
            if notify:
                old_body = db.get(body_name)
                diff = compare_bodies(
                    old_body, body.prettify().encode('utf-8'))
                to_notify.append((web, diff))
            date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            print("%s - %s: %s" % (date, hash_name, res))
            # Store new hash:
            db[hash_name] = new_hash
            db[body_name] = body.prettify().encode('utf-8')

    with MailServer() as smtp:
        for website, diff in to_notify:
            # each change implies 3 lines of diff.
            if diff.count("\n") / 3 < THRESHOLD:
                date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                print("%s - Changes for %s below threshold. Skip "
                      "notification." % (date, website))
                continue

            smtp.send_notification(website, diff)


if __name__ == "__main__":
    main()
