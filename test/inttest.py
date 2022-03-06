import pytest
import requests



def test_list():
    url = "http://localhost:21155/api/list"
    r = requests.get(url)
    list = r.token
    assert r.status_code == 200
    return list

def test_login():
    url = "http://localhost:21155/api/login"
    r = requests.post(url,data = {"login":"root","haslo":"root"})
    token = r.json['token']
    assert r.status_code == 200
    return token
def test_eventadd():
    url = "http://localhost:21155/api/eventadd"
    data = {"eventname":"TestAPI133333",
            "eventpersoncreator":"Damian",
            "eventstartdate":"2022-03-05 10:00",
            "eventstopdate":"2022-03-05 12:00",
            "descr":"test",
            "email":"test@test.pl"}
    r = requests.post(url,data)
    assert r.status_code == 200

def approve_test():
    login = test_login()
    id = test_list()
    for x in id:
        r = requests.post("http://localhost:21155/api/approve",headers={"Authorizaton":login['token']},body={"id":x})
        assert r.status_code == 200
        
