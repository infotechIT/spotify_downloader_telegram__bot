from __future__ import unicode_literals
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from youtube_search import YoutubeSearch
import youtube_dl
import eyed3.id3
import eyed3
import lyricsgenius
import telepot


spotifyy = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id='client id spotify',
                                                        client_secret='client secret spotify'))
genius = lyricsgenius.Genius('genius api token')

token = 'token bot'
bot = telepot.Bot(token)

def DOWNLOADMP3(link,chat_id):
    results = spotifyy.track(link)
    song = results['name']
    artist = results['artists'][0]['name']
    YTSEARCH = str(song + " " + artist)
    artistfinder = results['artists']
    tracknum = results['track_number']
    album = results['album']['name']
    realese_date = int(results['album']['release_date'][:4])
    if len(artistfinder) > 1:
        fetures = "( Ft."
        for lomi in range(0, len(artistfinder)):
            try:
                if lomi < len(artistfinder) - 2:
                    artistft = artistfinder[lomi + 1]['name'] + ", "
                    fetures += artistft
                else:
                    artistft = artistfinder[lomi + 1]['name'] + ")"
                    fetures += artistft
            except:
                pass
    else:
        fetures = ""

    time_duration = ""
    time_duration1 = ""
    time_duration2 = ""
    time_duration3 = ""
    millis = results['duration_ms']
    millis = int(millis)
    seconds = (millis / 1000) % 60
    minutes = (millis / (1000 * 60)) % 60
    seconds = int(seconds)
    minutes = int(minutes)
    if seconds >= 10:
        if seconds < 59:
            time_duration = "{0}:{1}".format(minutes, seconds)
            time_duration1 = "{0}:{1}".format(minutes, seconds + 1)
            time_duration2 = "{0}:{1}".format(minutes, seconds - 1)
            if seconds == 10:
                time_duration2 = "{0}:0{1}".format(minutes, seconds - 1)
                time_duration3 = "{0}:{1}".format(minutes, seconds + 2)
            elif seconds<58:
                time_duration3 = "{0}:{1}".format(minutes, seconds + 2)
                time_duration2 = "{0}:{1}".format(minutes, seconds - 1)
            elif seconds == 58:
                time_duration3 = "{0}:0{1}".format(minutes+1, seconds -58)
                time_duration2 = "{0}:{1}".format(minutes, seconds - 1)
            else:
                time_duration2 = "{0}:{1}".format(minutes, seconds - 1)
        else:
            time_duration1 = "{0}:0{1}".format(minutes + 1, seconds - 59)
            if seconds == 59:
                time_duration3 = "{0}:0{1}".format(minutes + 1, seconds - 58)
    else:
        time_duration = "{0}:0{1}".format(minutes, seconds)
        time_duration1 = "{0}:0{1}".format(minutes, seconds + 1)

        if seconds < 8:
            time_duration3 = "{0}:0{1}".format(minutes, seconds + 2)
            time_duration2 = "{0}:0{1}".format(minutes, seconds - 1)
        elif seconds ==9 or seconds==8:
            time_duration3 = "{0}:{1}".format(minutes, seconds + 2)

        elif seconds == 0:
            time_duration2 = "{0}:{1}".format(minutes - 1, seconds + 59)
            time_duration3 = "{0}:0{1}".format(minutes, seconds + 2)
        else:
            time_duration2 = "{0}:0{1}".format(minutes, seconds - 1)
            time_duration3 = "{0}:0{1}".format(minutes, seconds + 2)

    trackname = song + fetures

    response = requests.get(results['album']['images'][0]['url'])
    DIRCOVER = "songpicts//" + trackname + ".png"
    file = open(DIRCOVER, "wb")
    file.write(response.content)
    file.close()


    results = list(YoutubeSearch(str(YTSEARCH)).to_dict())
    LINKASLI = ''
    for URLSSS in results:
        timeyt = URLSSS["duration"]
        print(URLSSS['title'])
        if timeyt == time_duration or timeyt == time_duration1:
            LINKASLI = URLSSS['url_suffix']
            break
        elif timeyt == time_duration2 or timeyt == time_duration3:
            LINKASLI = URLSSS['url_suffix']
            break

    YTLINK = str("https://www.youtube.com/" + LINKASLI)
    print(YTLINK)

    options = {
        # PERMANENT options
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': f'song//{trackname}.*',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'
        }],

        # (OPTIONAL options)
        'noplaylist': True
    }

    with youtube_dl.YoutubeDL(options) as mp3:
        mp3.download([YTLINK])


    aud = eyed3.load(f"song//{trackname}.mp3")
    aud.tag.artist = artist
    aud.tag.album = album
    aud.tag.album_artist = artist
    aud.tag.title = trackname
    aud.tag.track_num = tracknum
    aud.tag.year = realese_date
    try:
        songok = genius.search_song(song, artist)
        aud.tag.lyrics.set(songok.lyrics)
    except:
        pass
    aud.tag.images.set(3, open("songpicts//" + trackname + ".png", 'rb').read(), 'image/png')
    aud.tag.save()
    bot.sendAudio(chat_id, open(f'song//{trackname}.mp3', 'rb'),title=trackname)



def album(link):
    results = spotifyy.album_tracks(link)
    albums = results['items']
    while results['next']:
        results = spotifyy.next(results)
        albums.extend(results['items'])
    return albums


def artist(link):
    results = spotifyy.artist_top_tracks(link)
    albums = results['tracks']
    return albums


def searchalbum(track):

    results = spotifyy.search(track)
    return results['tracks']['items'][0]['album']['external_urls']['spotify']

def playlist(link):
    results = spotifyy.playlist_tracks(link)
    return results['items']


def searchsingle(track):

    results = spotifyy.search(track)
    return results['tracks']['items'][0]['href']


def searchartist(searchstr):

    results = spotifyy.search(searchstr)
    return results['tracks']['items'][0]['artists'][0]["external_urls"]['spotify']


