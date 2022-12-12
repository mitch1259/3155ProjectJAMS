import unittest
import requests

class FlaskTest(unittest.TestCase):

    def test_user(self):
        response = requests.get("http://127.0.0.1:5000/user")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Welcome to JAMS' in response.text, True)
    
    def test_register(self):
        response = requests.get("http://127.0.0.1:5000/register")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<form method="POST" action="/register">' in response.text, True)
    
    def test_login(self):
        response = requests.get("http://127.0.0.1:5000/login")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(' <form method="POST" action="/login">' in response.text, True)

    def test_project(self):
        response = requests.get("http://127.0.0.1:5000/2?")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h1>Project Details</h1>' in response.text, True)
    
    def test_editproject(self):
        #editing the project
        response = requests.get("http://127.0.0.1:5000/1/edit")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<form action="/1/edit" method="post">' in response.text, True)

    def test_projectCreate(self):
        response = requests.get("http://127.0.0.1:5000/1?/create")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Project Details' in response.text, True)
    
    def test_createproject(self):
        response = requests.get("http://127.0.0.1:5000/user/createproject")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Project Name' in response.text, True)
    
    # def test_login(self):
    #     response = requests.get("http://127.0.0.1:5000/login")
    #     statuscode = response.status_code
    #     self.assertEqual(statuscode, 200)
    #     self.assertEqual(' <form method="POST" action="/login">' in response.text, True)
    
    def test_clock(self):
        response = requests.get("http://127.0.0.1:5000/clocklogic")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h1>You are currently clocked</h1>' in response.text, True)
    
    def test_github(self):
        response = requests.get("http://127.0.0.1:5000/login/github")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Welcome to JAMS' in response.text, True)

    def test_delete(self):
        response = requests.get('http://127.0.0.1:5000/delete/1')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

if __name__ == " __main__":
    unittest.main()