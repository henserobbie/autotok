from tiktok_uploader.upload import upload_video, upload_videos
from tiktok_uploader.auth import AuthBackend
from multiprocessing import Process, Queue
import pandas, pickle

class Poster:
    def run(postQueue, accounts):
        while True:
            try:
                job = postQueue[0]
            except:
                job = None
            if job != None:
                try:
                    i = accounts.index[accounts['username'] == job['username']].tolist()[0]
                    tags = accounts['tags'][i]
                    print('uploading video: ', job['title'])
                    Poster.upload(job['username'], job['filename'], job['title'], tags)
                    postQueue.pop(0)
                except:
                    print('failed to upload vid: ', job)
        return
    
    def upload(username, filename, title, tags):
        f = open(f'cookies/{username}.pkl', 'rb')
        cookies = pickle.load(f)
        f.close()
        upload_video(filename, description=f'{title} {tags}', cookies_list=cookies, headless=True)

if __name__ == "__main__":
    print('Sucess')