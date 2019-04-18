#!/usr/bin/env python3

import unittest
import sys
import requests
import uuid
import base64

host = "http://localhost:8010"
flag1 = "cheeky_bugger_u_aint_fixed_the_bug_innit"
flag2 = "absolute_lad_what_a_legend"

class TestBingDrive(unittest.TestCase):
    def test_check_permissions(self):
        s = requests.Session()
        rand = str(uuid.uuid4())
        s.post(f'{host}/register',json={'username': rand, 'password': rand})
        r = s.get(f'{host}/document/flag?r=QWRtaW4=')
        self.assertNotIn(flag1, r.text)
    
    def test_can_make_new_file(self):
        s = requests.Session()
        rand = str(uuid.uuid4())
        s.post(f'{host}/register',json={'username': rand, 'password': rand})
        s.post(f'{host}/upload', json={'name': 'A', 'text': rand})
        user = base64.b64encode(bytes(rand ,'utf-8')).decode('utf-8')
        r = s.get(f'{host}/document/A?r={user}')
        self.assertIn(rand, r.text)

    def test_cant_brute_force(self):
        s = requests.Session()
        blocked = False
        # shouldn't be allowed to keep trying till you get it
        for code in range(0,25):
            r = s.post(f'{host}/admin',data={'pin': f'{code:04}'})
            if r.status_code != 200:
                blocked = True
        # check that we got blocked at some point
        self.assertTrue(blocked)

    def test_can_use_admin_page(self):
        # can we still login at all lol
        s = requests.Session()
        r = s.post(f'{host}/admin',data={'pin': f'2941'})
        self.assertIn(flag2, r.text)

    def test_no_sqli(self):
        s = requests.Session()
        s.post(f'{host}/login',json={'username': 'testStaff', 'password': 'testStaff'})
        r = s.get(f'{host}/api/peek/file?file_id=\'')
        self.assertNotEqual(r.status_code, 500)
        r = s.get(f"{host}/api/peek/file?file_id=123456678%20UNION%20SELECT%20NULL,NULL,NULL,load_file(%27/var/log/messages%27)")
        self.assertEqual(r.text,":(")

    def test_peek_still_works(self):
        s = requests.Session()
        s.post(f'{host}/login',json={'username': 'testStaff', 'password': 'testStaff'})
        r = s.get(f'{host}/api/peek/file?file_id=1')
        self.assertIn(flag1, r.text)

if __name__ == "__main__":
    unittest.main()