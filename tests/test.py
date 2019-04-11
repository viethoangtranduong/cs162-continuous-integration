import os
import requests
import unittest
from sqlalchemy import create_engine

class DockerComposeTestCase(unittest.TestCase):

    def test_endpoint(self):
        r = requests.post('http://127.0.0.1:5000/add', data={'expression':'100+100'})
        self.assertEqual(r.status_code, 200)

    def test_error_endpoint(self):
        r = requests.post('http://127.0.0.1:5000/add', data={'expression':'100+'})
        self.assertNotEqual(r.status_code, 200)

    def test_db(self):
        r = requests.post('http://127.0.0.1:5000/add', data={'expression':'100+100'})
        engine = create_engine('postgresql://cs162_user:cs162_password@127.0.0.1:5432/cs162', echo = True)

        with engine.connect() as con:
            rs = con.execute("SELECT * FROM Expression WHERE text = '100+100'")
            rows = rs.fetchall()

        self.assertNotEqual(len(rows), 0)

    def test_error_db(self):
        r = requests.post('http://127.0.0.1:5000/add', data={'expression':'100+'})
        engine = create_engine('postgresql://cs162_user:cs162_password@127.0.0.1:5432/cs162', echo = True)

        with engine.connect() as con:
            rs = con.execute("SELECT * FROM Expression WHERE text = '100+'")
            rows = rs.fetchall()

        self.assertEqual(len(rows), 0)

if __name__ == '__main__':
    unittest.main()