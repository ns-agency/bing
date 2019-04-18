#!/usr/bin/env python3

import unittest
import sys
import requests
import uuid
import base58 
import re

def dist(a, b):
    diff = 0
    for i in range(0,min(len(a),len(b))):
        if a[i] != b[i]:
            diff += 1
    return diff + abs(len(a) - len(b))

host = "http://localhost:8009"
class TestPasteBing(unittest.TestCase):
    # Can we guess the ID of a post
    def test_idor_basic(self):
        s = requests.Session()
        rand = str(uuid.uuid4())
        s.post(f'{host}/register',data={'username': rand, 'password': rand})
        s.post(f'{host}/new', data={'title': rand, 'contents': rand})
        for i in range(10):
            code = base58.b58encode(f"{i}:1").decode("UTF-8")
            r = s.get(f'{host}/raw/{code}')
            self.assertNotIn(rand, r.text)
        
    # are the paste ids super related
    def test_unique_ids(self):
        s = requests.Session()
        rand = str(uuid.uuid4())
        s.post(f'{host}/register',data={'username': rand, 'password': rand})
        s.post(f'{host}/new', data={'title': rand, 'contents': rand})
        s.post(f'{host}/new', data={'title': rand, 'contents': rand})
        r = s.get(f'{host}/pastes')
        links = re.findall(r'/raw/[a-zA-Z0-9_-]+', r.text)
        self.assertEqual(len(links), 2)
        links = [link.split('/')[-1] for link in links]
        # there should be _at_ least 3 different characters between the ids
        self.assertGreater(dist(links[0],links[1]), 2)
        
    # The point of pastebing is you can share links
    # So make sure you can still do that
    def test_can_share(self):
        # user 1
        s = requests.Session()
        rand = str(uuid.uuid4())
        s.post(f'{host}/register',data={'username': rand, 'password': rand})
        s.post(f'{host}/new', data={'title': rand, 'contents': rand})
        r = s.get(f'{host}/pastes')
        link = re.search(r'/raw/[a-zA-Z0-9_-]+', r.text)
        self.assertIsNotNone(link)
        link = link.group(0)

        # user 2
        s2 = requests.Session()
        rand2 = str(uuid.uuid4())
        s2.post(f'{host}/register',data={'username': rand2, 'password': rand2})
        r = s2.get(f'{host}{link}')
        self.assertIn(rand, r.text)

if __name__ == "__main__":
    unittest.main()