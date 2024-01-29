from googleapiclient.discovery import build
import random

class ContentFinder:
    def query(searchterms, blacklist):
        api_key = 'your youtube api key'
        # Create a YouTube Data API client
        youtube = build('youtube', 'v3', developerKey=api_key)
        # Define search
        searches = [string.strip() for string in searchterms.split(',')]
        search = random.choice(searches)
        perPage = 10
        # Initial Search
        search_response = youtube.search().list(
            q=search,
            type='video',
            part='id,snippet',
            maxResults=perPage
        ).execute()
        print('one query executed')
        for search_result in search_response.get('items', []):
            video_id = search_result['id']['videoId']
            video_title = search_result['snippet']['title']
            if video_id not in blacklist:
                return({'id':video_id, 'title':video_title, 'duration':999}) #add duration support
        nextPage = search_response.get("nextPageToken", '')
        while True:
            search = random.choice(searches)
            search_response = youtube.search().list(
                q=search,
                type='video',
                part='id,snippet',
                maxResults=perPage,
                pageToken=nextPage
            ).execute()
            print('another query executed')
            for search_result in search_response.get('items', []):
                video_id = search_result['id']['videoId']
                video_title = search_result['snippet']['title']
                if video_id not in blacklist:
                    return({'id':video_id, 'title':video_title, 'duration':999}) #add duration support
            nextPage = search_response.get('nextPageToken', '')
