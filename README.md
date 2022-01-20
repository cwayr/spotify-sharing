# Spotify Sharing

![Code Coverage](coverage.svg) [![Maintainability](https://api.codeclimate.com/v1/badges/a315edd27ca938e099b4/maintainability)](https://codeclimate.com/github/cwaymeyer/spotify-sharing/maintainability) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/0640eac1afb1428ca2375fbce7529141)](https://www.codacy.com/gh/cwaymeyer/spotify-sharing/dashboard?utm_source=github.com&utm_medium=referral&utm_content=cwaymeyer/spotify-sharing&utm_campaign=Badge_Grade)

An app for sharing music with friends.

Built with Python, Flask, SQLAlchemy, PostgreSQL, HTML/Jinja, CSS, JavaScript.

This app makes use of [Spotify's web API](https://developer.spotify.com/documentation/web-api/).

Users can sign up and create and join groups. Groups are made up of a post feed, where users can share songs with each other. Posts are likeable and the most-liked songs will be displayed in a list on the group page.
<br />

<hr />

## To get Started (💻 Dev)

<br />
Run in terminal:

- `git clone https://github.com/cwaymeyer/spotify-sharing.git` (clone repository)
- `cd spotify-sharing` (cd into folder)
- `python3 -m venv venv` (create virtual environment)
- `source ven/bin/activate` (activate virtual environment)
- `pip3 install -r requirements.txt` (install requirements)
- `createdb spotify-sharing` (create database) (`createdb spotify-sharing-test` for test db)
- `touch api_keys.py`
  > Inside of `api_keys.py`, set following variables:
  >
  > - `CLIENT_ID = {Client ID}`
  > - `CLIENT_SECRET = {Client Secret}`
  > 
  >   Both Client ID and Client Secret can be acquired through [Spotify's Web API](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/)
- `flask run` (run application)

#### Testing

- To test application, run `python3 -m unittest discover tests/` from root directory
<br />
<hr />

## Database Schema

<br />
<img src="./static/images/db_diagram.jpg" width="800"/>

(Database diagram created with [dbdiagram.io](https://dbdiagram.io/home))
</br >

<hr />

## Demo Screenshots

<br />
<img src="./static/images/group_page_demo.jpg" width="700">
<img src="./static/images/spotify_search_demo.jpg" width="700">
<img src="./static/images/user_page_demo.jpg" width="700">
