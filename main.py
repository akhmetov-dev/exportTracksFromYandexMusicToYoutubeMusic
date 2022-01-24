import getpass
from yandex_music import Client
from ytmusicapi import YTMusic

# Алгоритм работы скрипта:
# 1) получение списка лайканных треков из Яндекс.Музыки
# 2) поиск трека на ютубе методом ytmusic.get_song() и получение VideoId из объекта videoDetails
# 3) добавление трека в целевой плейлист
# 4) переход в 2) пока все треки не будут найдены

login = input("Login: ")
password = getpass.getpass("Password: ")

youtubeClient = YTMusic('headers_auth.json')
yandexClient = Client.from_credentials(login, password)

# Получение списка названий любимых треков
##########################################
yandexLikedTracks = yandexClient.users_likes_tracks().fetch_tracks()

# Поиск максимально похожего трека (категория : песни) в youtube music (по сочетанию название + артисты)
##########################################
for yandexLikedTrack in yandexLikedTracks:
    artists = ""
    for artist in yandexLikedTrack.artists:
        artists += artist.name + " "
    youtubeSearchingResults = youtubeClient.search(yandexLikedTrack.title + " " + artists)
    if(youtubeSearchingResults.__len__() > 0):
        for youtubeChapter in youtubeSearchingResults:
            if(youtubeChapter.get("category") == "Songs"):
                tracksToAdd = list()
                tracksToAdd.append(youtubeChapter.get("videoId"))
                print(youtubeChapter.get("title"))
                youtubeClient.add_playlist_items("VLPLZqP2fvb9Bhy8N4BHLcLU5KnPx9QpgmLK", tracksToAdd)
                break