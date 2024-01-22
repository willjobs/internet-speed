# `internet-speed`

This is a simple project used to monitor the internet speed. When `main.py` is run, it will run a speed test of the download and upload speeds, save them to a file in `data/speed_tests.txt` (appending if it already exists) and uploading it a file on Dropbox.

Resources I used to get this working:
* [This SO answer](https://stackoverflow.com/a/23895259/1102199) explains how to create an app in dropbox. Don't worry about the "generate access token" step. The main things to focus on are (1) copying the `App key` and `App secret` and (2) going to the Permissions tab and making sure to check `files.content.write` and `files.content.read`.
* [This SO answer](https://stackoverflow.com/a/71794390/1102199) explains how to use the `App key` and `App secret` to get the OAuth2 refresh token that is needed to avoid having to continually get new access tokens (the "generate access token" button on the dropbox site gives you a "short-lived" token which lasts ~ 4 hours).
* [This SO answer](https://stackoverflow.com/a/42143895/1102199) is what I started with and modified to get it to its current state.
