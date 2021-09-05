from youtube import Youtube

y = Youtube('AIzaSyCqwqA1Mn7zF5rJOX67qjWLd72B319r8Tw',
            'https://youtube.googleapis.com/youtube/v3/')

print('here')
playlists = y.get_all_playlists('snippet','UCEBb1b_L6zDS3xTUrIALZOw')
playlists_videos = y.get_all_playlist_videos('snippet',playlists)