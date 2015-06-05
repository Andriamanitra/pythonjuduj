import requests
from xml.etree import ElementTree as ET
import datetime


def np(username):
    r = requests.get("http://ws.audioscrobbler.com/1.0/user/%s/recenttracks.rss" % username)
    if r.status_code == requests.codes.ok:
        try:
            lastfm = ET.fromstring(r.text)
            now_playing = lastfm[0][9][0].text
            play_time = datetime.datetime.strptime(lastfm[0][9][2].text, "%a, %d %b %Y %H:%M:%S +0000")
            tz = datetime.datetime.now() - datetime.datetime.utcnow()
            play_time = play_time + tz
            aika = play_time.strftime("%d.%m.%Y @ %H:%M")
            link = lastfm[0][9][3].text
            if play_time > ( datetime.datetime.now() - datetime.timedelta(minutes=8) ):
                return "Last.fm: {0} is now playing {1} | Link: {2}".format(username, now_playing, link)
            else:
                return "Last.fm: {0} last listened to: {1} ({2}) | Link: {3}".format(username, now_playing, aika, link)
        except IndexError:
            return "No tracks found for user " + username
    else:
        return "Username not found"

