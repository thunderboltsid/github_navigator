import json
import logging
import os

from flask import Flask, request
import requests

app = Flask(__name__)

_GLOBALS = {
        "api_root": "https://api.github.com",
        "search_root": "search/repositories",
        "search_params": {
            "sort": "updated",
            "order": "desc",
            "per_page": "5",
            "client_id": os.environ.get("GITHUB_CLIENT_ID"),
            "client_secret": os.environ.get("GITHUB_CLIENT_SECRET")
            },
        }


class User(object):
    def __init__(self, name=None, url=None, avatar=None, username=None, email=None):
        self._name = name
        self._url = url
        self._avatar = avatar
        self._username = username
        self._email = email

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @property
    def avatar(self):
        return self._avatar

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email


class Commit(object):
    def __init__(self, url=None, timestamp=None, message=None, author=None, sha=None):
        self._url = url
        self._timestamp = timestamp
        self._message = message
        self._author = author
        self._hash = sha

    @property
    def sha(self):
        return self._hash

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def message(self):
        return self._message

    @property
    def author(self):
        return self._author

    @property
    def url(self):
        return self._url


class Repository(object):
    def __init__(self, url=None, name=None, owner=None):
        self._url = url
        self._name = name
        self._owner = owner

    @property
    def name(self):
        return self._name

    @property
    def owner(self):
        return self._owner

    @property
    def url(self):
        return self._url

    def last_commit(self):
        url_string = "https://api.github.com/repos/{}/{}/commits".format(self._owner.username, self._name)
        payload = {}
        for key, value in _GLOBALS["search_params"].items():
            payload[key] = value
        response = requests.get(url_string, params=payload)
        if response.status_code == 200:
            content = json.loads(response.text)
        else:
            logging.debug("request for url ({}) returned status code: {}".format(url_string, response.status_code))
        commit = content[0]
        author = commit["author"]
        if author is None:
            author = commit["commit"]["author"]
            author["html_url"] = ""
            author["avatar_url"] = ""
            author["login"] = ""
        author = User(username=author["login"],
                      url=author["html_url"],
                      avatar=author["avatar_url"],
                      name=commit["commit"]["author"]["name"],
                      email=commit["commit"]["author"]["email"])
        commit = Commit(url=commit["html_url"],
                        timestamp=commit["commit"]["author"]["date"], 
                        message=commit["commit"]["message"],
                        sha=commit["sha"],
                        author=author)
        return commit



@app.route("/")
def home():
    return "Github Navigator"


@app.route("/navigator/", methods=["GET"])
def navigator():
    repos = []
    search_term = request.args.get("search_term", "")
    payload = {
        "q": search_term
    }
    for key, value in _GLOBALS["search_params"].items():
        payload[key] = value
    url_string = "{}/{}?".format(
            _GLOBALS["api_root"],
            _GLOBALS["search_root"])
    response = requests.get(url_string, params=payload)

    if response.status_code == 200:
        content = json.loads(response.text)
    else:
        logging.debug("Search request returned status code: {}".format(response.status_code))
        import pdb; pdb.set_trace()

    for item in content["items"]:
        author = User(username=item["owner"]["login"],
                      url=item["owner"]["html_url"],
                      avatar=item["owner"]["avatar_url"])
        repos.append(Repository(url=item["html_url"],
                                name=item["name"],
                                owner=author))
    resp = ""

    for repo in repos:
        resp += "Repository Name: <a href='{}'>{}</a><br>Owner: <a href='{}'>{}</a><br><br>".format(
            repo.url, repo.name, repo.owner.url, repo.owner.username)
        last_commit = repo.last_commit()
        resp += "Last Commit: <a href='{}'>{}</a><br>{}<br><a href='{}'><img src='{}' width='30px' height='30px'></a> {}<br><br>".format(
            last_commit.url, last_commit.sha, last_commit.message, last_commit.author.url, last_commit.author.avatar, last_commit.author.name)
        resp += "<hr>"
        resp += "<br>"


    return resp


if __name__ == "__main__":
    if _GLOBALS["search_params"]["client_id"] is None:
        logging.debug("Environment variable 'GITHUB_CLIENT_ID' not present. Unable to use authorized API.")
    if _GLOBALS["search_params"]["client_secret"] is None:
        logging.debug("Environment variable 'GITHUB_CLIENT_SECRET' not present. Unable to use authorized API.")
    app.run()

